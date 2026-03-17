import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Auto Shop Analytics", page_icon="🚗", layout="wide")

st.title("🚗 Auto Shop Analytics & AI Dashboard")
st.write("Live data streaming directly from Supabase.")

try:
    # Connect to Supabase using Streamlit's native SQL connection
    conn = st.connection("supabase", type="sql")
except Exception as e:
    st.error(f"❌ Connection failed. Ensure .streamlit/secrets.toml is configured correctly. Error: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("📅 Filter Historical Data")
start_date = st.sidebar.date_input("Start Date", date(2018, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2026, 12, 31))
st.sidebar.info("Adjust these dates to see older Excel data!")

st.divider()

# --- DATA TABLES ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Employee Requisitions")
    try:
        req_df = conn.query(f"""
            SELECT t.id, e.name as employee, m.item_name as material, t.quantity, t.created_at
            FROM transactions t
            JOIN employees e ON t.employee_id = e.id
            JOIN materials m ON t.material_id = m.id
            WHERE t.created_at >= '{start_date}' AND t.created_at <= '{end_date}'
            ORDER BY t.created_at DESC LIMIT 50;
        """, ttl="1m")
        st.dataframe(req_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.info("No transaction data available yet.")

with col2:
    st.subheader("💰 Supplier Purchases")
    try:
        pur_df = conn.query(f"""
            SELECT p.id, m.item_name, p.supplier_name, p.quantity, p.total_amount, p.purchase_date
            FROM purchases p
            JOIN materials m ON p.material_id = m.id
            WHERE p.purchase_date >= '{start_date}' AND p.purchase_date <= '{end_date}'
            ORDER BY p.purchase_date DESC LIMIT 50;
        """, ttl="1m")
        st.dataframe(pur_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.info("No purchase data available yet.")

# --- CHARTS ---
st.divider()
st.subheader("📈 Purchase Trends (Total Amount Spend)")

if 'pur_df' in locals() and not pur_df.empty:
    # Convert date column and group by date to get daily spend
    pur_df['purchase_date'] = pd.to_datetime(pur_df['purchase_date'])
    chart_data = pur_df.groupby('purchase_date')['total_amount'].sum().reset_index()
    chart_data.set_index('purchase_date', inplace=True)
    
    st.line_chart(chart_data)
else:
    st.info("No purchase data found in this date range to chart.")