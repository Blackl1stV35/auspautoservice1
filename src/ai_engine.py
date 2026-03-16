import pandas as pd
from sklearn.ensemble import IsolationForest
from prophet import Prophet
from src.config import supabase, logger

def fetch_table(table_name):
    res = supabase.table(table_name).select("*").execute()
    return pd.DataFrame(res.data)

def run_ai_analysis():
    logger.info("Initializing AI Engine...")
    
    # 1. Anomaly Detection
    df_purchases = fetch_table("purchases")
    if not df_purchases.empty:
        model = IsolationForest(contamination=0.05, random_state=42)
        X = df_purchases[['price_per_unit']].fillna(0)
        df_purchases['anomaly_score'] = model.fit_predict(X)
        
        anomalies = df_purchases[df_purchases['anomaly_score'] == -1]
        logger.info(f"Found {len(anomalies)} price anomalies.")
        for _, row in anomalies.iterrows():
             logger.warning(f"ANOMALY: Material ID {row['material_id']} from {row['supplier_name']} at {row['price_per_unit']} THB (Date: {row['purchase_date']})")

    # 2. Demand Forecasting (Example for highly used materials)
    df_trans = fetch_table("transactions")
    if not df_trans.empty:
        # Get the most used material ID for a sample forecast
        top_material = df_trans['material_id'].value_counts().idxmax()
        df_mat = df_trans[df_trans['material_id'] == top_material].copy()
        
        df_mat['ds'] = pd.to_datetime(df_mat['created_at']).dt.date
        df_mat['y'] = df_mat['quantity']
        daily_usage = df_mat.groupby('ds')['y'].sum().reset_index()

        if len(daily_usage) >= 2: # Prophet needs at least 2 data points
            m = Prophet(daily_seasonality=True, yearly_seasonality=False)
            m.fit(daily_usage)
            future = m.make_future_dataframe(periods=7)
            forecast = m.predict(future)
            logger.info(f"Forecast for Material ID {top_material} next 7 days:\n" + forecast[['ds', 'yhat']].tail(7).to_string(index=False))