import sys
import io
import os
import pandas as pd
import numpy as np
import re
from supabase import create_client, Client
from sklearn.ensemble import IsolationForest
from prophet import Prophet
from dotenv import load_dotenv

# Route all print() output to a log file to avoid Windows encoding errors in terminal
log_file = open('output_log.txt', 'w', encoding='utf-8')
sys.stdout = log_file
sys.stderr = log_file

load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# ==========================================
# PART 1: DATA INGESTION (ETL)
# ==========================================

def clean_quantity(val):
    """Cleans messy text inputs like '3+' or ' 2 ' into integers."""
    if pd.isna(val) or val == '':
        return 0
    numbers = re.findall(r'\d+', str(val))
    return int(numbers[0]) if numbers else 0

def fix_thai_date(dt):
    """Fixes the 2-digit Thai year bug (e.g., '67' becomes 1967 -> converted to 2024)."""
    if pd.isnull(dt):
        return dt
    if isinstance(dt, str):
        try:
            dt = pd.to_datetime(dt)
        except:
            return dt
    # If pandas read '67' as 1967, add 57 years to make it 2024
    if hasattr(dt, 'year') and dt.year < 2000:
        try:
            return dt.replace(year=dt.year + 57)
        except ValueError:
            return dt
    return dt

def process_requisitions_excel(file_path):
    """Processes employee material requisitions."""
    print(f"\n[1/2] Processing Requisitions File: {file_path}")
    xls = pd.ExcelFile(file_path)
    
    for sheet_name in xls.sheet_names:
        if "ฟอร์มเปล่า" in sheet_name:
            continue
            
        print(f"  -> Reading sheet: {sheet_name}")
        # header=0 reads the actual material names as columns
        df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
        
        if df.empty or len(df.columns) < 2:
            continue

        # Rename the first column to Employee_Name
        df.rename(columns={df.columns[0]: 'Employee_Name'}, inplace=True)
        
        # Drop the first row which contains the 1, 2, 3... counting numbers
        df = df.drop(index=0)
        
        df_melted = df.melt(id_vars=['Employee_Name'], var_name='Material_Name', value_name='Quantity')
        df_melted['Quantity'] = df_melted['Quantity'].apply(clean_quantity)
        
        # Keep only actual withdrawals
        df_melted = df_melted[df_melted['Quantity'] > 0] 
        df_melted.dropna(subset=['Employee_Name', 'Material_Name'], inplace=True)
        
        # Filter out rows where Employee_Name contains 'เดือน' (Month)
        df_melted = df_melted[~df_melted['Employee_Name'].astype(str).str.contains('เดือน')]

        for index, row in df_melted.iterrows():
            emp_name = str(row['Employee_Name']).strip()
            mat_name = str(row['Material_Name']).strip()
            qty = row['Quantity']
            
            print(f"     [Inserting] Employee: {emp_name} took {mat_name}, Qty: {qty}")
            
            # 1. หาหรือสร้าง Employee ID
            emp_res = supabase.table("employees").select("id").eq("name", emp_name).execute()
            if not emp_res.data:
                emp_res = supabase.table("employees").insert({"name": emp_name}).execute()
            emp_id = emp_res.data[0]['id']

            # 2. หาหรือสร้าง Material ID
            mat_res = supabase.table("materials").select("id").eq("item_name", mat_name).execute()
            if not mat_res.data:
                mat_res = supabase.table("materials").insert({"item_name": mat_name}).execute()
            mat_id = mat_res.data[0]['id']

            # 3. บันทึก Transaction ลง Database จริง
            supabase.table("transactions").insert({
                "employee_id": emp_id,
                "material_id": mat_id,
                "quantity": qty
            }).execute()

def process_purchasing_excel(file_path):
    """Processes purchasing and cost files."""
    print(f"\n[2/2] Processing Purchasing File: {file_path}")
    xls = pd.ExcelFile(file_path)
    
    for sheet_name in xls.sheet_names:
        if "สรุปยอด" in sheet_name:
            continue 
            
        print(f"  -> Reading sheet: {sheet_name}")
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        column_mapping = {
            'รายการ': 'Material_Name', 'ชื่อร้าน': 'Supplier_Name', 
            'จำนวน': 'Quantity', 'ราคา/ชิ้น': 'Price_Per_Unit', 
            'รวมจำนวนเงิน': 'Total_Amount', 'ว/ด/ป': 'Purchase_Date'
        }
        df.rename(columns=column_mapping, inplace=True)
        
        cols_to_keep = list(column_mapping.values())
        df = df[[c for c in cols_to_keep if c in df.columns]].dropna(subset=['Material_Name', 'Total_Amount'])
        
        if 'Quantity' in df.columns:
            df['Quantity'] = df['Quantity'].apply(clean_quantity)
        
        for index, row in df.iterrows():
            mat_name = str(row['Material_Name']).strip()
            raw_date = row.get('Purchase_Date')
            clean_date = fix_thai_date(raw_date)
            date_val = clean_date.strftime('%Y-%m-%d') if pd.notnull(clean_date) else None
            
            print(f"     [Inserting] Bought {mat_name} from {row.get('Supplier_Name', 'N/A')}")
            
            # 1. หาหรือสร้าง Material ID
            mat_res = supabase.table("materials").select("id").eq("item_name", mat_name).execute()
            if not mat_res.data:
                mat_res = supabase.table("materials").insert({"item_name": mat_name}).execute()
            mat_id = mat_res.data[0]['id']

            # 2. บันทึกข้อมูลการซื้อลง Database จริง
            supabase.table("purchases").insert({
                "material_id": mat_id,
                "supplier_name": str(row.get('Supplier_Name', '')),
                "quantity": row.get('Quantity', 0),
                "price_per_unit": row.get('Price_Per_Unit', 0),
                "total_amount": row.get('Total_Amount', 0),
                "purchase_date": date_val
            }).execute()

# ==========================================
# PART 2: AI / ML ANALYTICS
# ==========================================

def fetch_data(table_name):
    """Fetches data from Supabase for analysis."""
    response = supabase.table(table_name).select("*").execute()
    return pd.DataFrame(response.data)

def detect_anomalies():
    """Detects price anomalies using Isolation Forest."""
    print("\n[AI] Running Price Anomaly Detection...")
    df_purchases = fetch_data("purchases")
    
    if df_purchases.empty:
        return print("  -> No purchase data found in database.")

    model = IsolationForest(contamination=0.05, random_state=42)
    X = df_purchases[['price_per_unit']].fillna(0)
    df_purchases['anomaly_score'] = model.fit_predict(X)
    
    anomalies = df_purchases[df_purchases['anomaly_score'] == -1]
    
    for index, row in anomalies.iterrows():
        print(f"  [ANOMALY] Material ID {row['material_id']} from {row['supplier_name']} at {row['price_per_unit']} THB (Date: {row['purchase_date']})")

def forecast_demand(material_id=1):
    """Forecasts future material demand using Prophet."""
    print(f"\n[AI] Running Demand Forecasting for Material ID: {material_id}...")
    df_trans = fetch_data("transactions")
    
    if df_trans.empty:
        return print("  -> No transaction data found in database.")

    df_mat = df_trans[df_trans['material_id'] == material_id].copy()
    if df_mat.empty:
        return print(f"  -> No transaction history for Material ID {material_id}.")

    df_mat['ds'] = pd.to_datetime(df_mat['created_at']).dt.date
    df_mat['y'] = df_mat['quantity']
    daily_usage = df_mat.groupby('ds')['y'].sum().reset_index()

    m = Prophet(daily_seasonality=True, yearly_seasonality=False)
    m.fit(daily_usage)
    future = m.make_future_dataframe(periods=7) 
    forecast = m.predict(future)

    print("  [FORECAST] Predicted usage for next 7 days:")
    print(forecast[['ds', 'yhat']].tail(7).to_string(index=False))

# ==========================================
# PART 3: MAIN EXECUTION PIPELINE
# ==========================================
if __name__ == "__main__":
    print("Starting Data Pipeline & AI Analysis...")
    
    FILE_PURCHASES = r"data\3--เอสพี--ต้นทุนแผนกสี และน้ำมัน และกิ๊บน๊อต.xlsx"
    FILE_REQUISITIONS = r"data\เอสพี--สถิติเบิกวัสดุสิ้นเปลือง(69).xlsx"
    
    # 1. Run ETL
    try:
        if os.path.exists(FILE_REQUISITIONS):
            process_requisitions_excel(FILE_REQUISITIONS)
        else:
            print(f"[ERROR] File not found: {FILE_REQUISITIONS}")
            
        if os.path.exists(FILE_PURCHASES):
            process_purchasing_excel(FILE_PURCHASES)
        else:
            print(f"[ERROR] File not found: {FILE_PURCHASES}")
    except Exception as e:
        print(f"[ERROR] Exception during data ingestion: {e}")

    # 2. Run AI Analysis
    print("\n==========================================")
    print("Data Ingestion Complete -> Starting AI Analysis")
    print("==========================================")
    
    try:
        detect_anomalies()
        forecast_demand(material_id=1) 
    except Exception as e:
        print(f"[ERROR] Exception during AI Analysis: {e}")
        
    print("\nProcess finished successfully!")