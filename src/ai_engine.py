import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from src.config import supabase, logger

def fetch_table(table_name):
    res = supabase.table(table_name).select("*").execute()
    return pd.DataFrame(res.data)

def run_ai_analysis():
    logger.info("Initializing AI Engine...")
    
    # 1. Anomaly Detection (Isolation Forest)
    df_purchases = fetch_table("purchases")
    if not df_purchases.empty:
        model = IsolationForest(contamination=0.05, random_state=42)
        X = df_purchases[['price_per_unit']].fillna(0)
        df_purchases['anomaly_score'] = model.fit_predict(X)
        
        anomalies = df_purchases[df_purchases['anomaly_score'] == -1]
        logger.info(f"Found {len(anomalies)} price anomalies.")
        for _, row in anomalies.iterrows():
             logger.warning(f"ANOMALY: Material ID {row['material_id']} from {row['supplier_name']} at {row['price_per_unit']} THB (Date: {row['purchase_date']})")

    # 2. Demand Forecasting (Option A: Scikit-Learn Linear Regression)
    logger.info("Running Demand Forecasting (Linear Regression)...")
    df_trans = fetch_table("transactions")
    
    if not df_trans.empty:
        # Get the most used material ID for a sample forecast
        top_material = df_trans['material_id'].value_counts().idxmax()
        df_mat = df_trans[df_trans['material_id'] == top_material].copy()
        
        # Group by date to get daily usage
        df_mat['date'] = pd.to_datetime(df_mat['created_at']).dt.date
        daily_usage = df_mat.groupby('date')['quantity'].sum().reset_index()

        if len(daily_usage) >= 3: # Need a few data points to draw a trendline
            # Convert dates to numbers so the ML model can read them
            daily_usage['date_ordinal'] = pd.to_datetime(daily_usage['date']).map(pd.Timestamp.toordinal)
            
            X = daily_usage[['date_ordinal']]
            y = daily_usage['quantity']

            # Train the Linear Regression model
            lr_model = LinearRegression()
            lr_model.fit(X, y)

            # Predict the next 7 days
            last_date = pd.to_datetime(daily_usage['date'].max())
            future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 8)]
            future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
            
            forecast = lr_model.predict(future_ordinals)

            logger.info(f"--- 7-Day Forecast for Top Material (ID: {top_material}) ---")
            for i, date_obj in enumerate(future_dates):
                # Ensure we don't predict negative quantities
                pred_qty = max(0, round(forecast[i], 2))
                logger.info(f"Date: {date_obj.date()} -> Predicted Demand: {pred_qty} units")
        else:
            logger.warning("Not enough transaction data to run forecasting. Need at least 3 days of data.")