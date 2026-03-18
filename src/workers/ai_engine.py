import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from src.core.config import supabase, logger
from datetime import date, timedelta

def fetch_table(table_name):
    res = supabase.table(table_name).select("*").execute()
    return pd.DataFrame(res.data)

def run_ai_analysis():
    logger.info("Initializing AI Engine & Clearing old insights...")
    # Clear old insights before running
    supabase.table("ai_insights").delete().neq("id", 0).execute()
    
    df_purchases = fetch_table("purchases")
    df_trans = fetch_table("transactions")
    insights_to_insert = []

    # 1. Anomaly Detection (Isolation Forest)
    if not df_purchases.empty:
        model = IsolationForest(contamination=0.05, random_state=42)
        X = df_purchases[['price_per_unit']].fillna(0)
        df_purchases['anomaly_score'] = model.fit_predict(X)
        
        anomalies = df_purchases[df_purchases['anomaly_score'] == -1]
        logger.info(f"Found {len(anomalies)} price anomalies.")
        
        for _, row in anomalies.iterrows():
            insights_to_insert.append({
                "insight_type": "anomaly",
                "material_id": row['material_id'],
                "description": f"Suspicious price from {row['supplier_name']}",
                "metric_value": row['price_per_unit'],
                "insight_date": row['purchase_date']
            })

    # 2. Demand Forecasting (Linear Regression)
    if not df_trans.empty:
        top_material = df_trans['material_id'].value_counts().idxmax()
        df_mat = df_trans[df_trans['material_id'] == top_material].copy()
        df_mat['date'] = pd.to_datetime(df_mat['created_at']).dt.date
        daily_usage = df_mat.groupby('date')['quantity'].sum().reset_index()

        if len(daily_usage) >= 3:
            daily_usage['date_ordinal'] = pd.to_datetime(daily_usage['date']).map(pd.Timestamp.toordinal)
            X = daily_usage[['date_ordinal']]
            y = daily_usage['quantity']

            lr_model = LinearRegression()
            lr_model.fit(X, y)

            last_date = pd.to_datetime(daily_usage['date'].max())
            for i in range(1, 8):
                future_date = last_date + pd.Timedelta(days=i)
                pred_qty = max(0, round(lr_model.predict([[future_date.toordinal()]])[0], 2))
                
                insights_to_insert.append({
                    "insight_type": "forecast",
                    "material_id": int(top_material),
                    "description": "7-Day Predicted Demand",
                    "metric_value": pred_qty,
                    "insight_date": future_date.strftime('%Y-%m-%d')
                })

    # 3. Cost Optimization (Cheapest Supplier Logic)
    if not df_purchases.empty:
        # Find the cheapest supplier for each material
        cheapest_suppliers = df_purchases.loc[df_purchases.groupby('material_id')['price_per_unit'].idxmin()]
        for _, row in cheapest_suppliers.iterrows():
             insights_to_insert.append({
                "insight_type": "cost_optimization",
                "material_id": row['material_id'],
                "description": f"Optimal Supplier: {row['supplier_name']}",
                "metric_value": row['price_per_unit'],
                "insight_date": date.today().strftime('%Y-%m-%d')
            })

    # Batch Insert into Supabase
    if insights_to_insert:
        # Chunking to avoid payload too large
        for i in range(0, len(insights_to_insert), 500):
            supabase.table("ai_insights").insert(insights_to_insert[i:i+500]).execute()
        logger.info("✅ AI Insights successfully pushed to Supabase!")