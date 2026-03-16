import pandas as pd
import re
import concurrent.futures
from src.config import logger
from src.db_operations import get_or_create_employee, get_or_create_material, batch_insert

def clean_quantity(val):
    if pd.isna(val) or val == '':
        return 0
    numbers = re.findall(r'\d+', str(val))
    return int(numbers[0]) if numbers else 0

def fix_thai_date(dt):
    if pd.isnull(dt):
        return None
    if isinstance(dt, str):
        try:
            dt = pd.to_datetime(dt)
        except:
            return None
    if hasattr(dt, 'year') and dt.year < 2000:
        try:
            return dt.replace(year=dt.year + 57)
        except ValueError:
            return dt
    return dt

def process_requisition_sheet(xls, sheet_name):
    """Worker function for threading"""
    if "ฟอร์มเปล่า" in sheet_name:
        return []
    
    df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
    if df.empty or len(df.columns) < 2:
        return []

    df.rename(columns={df.columns[0]: 'Employee_Name'}, inplace=True)
    df = df.drop(index=0)
    df_melted = df.melt(id_vars=['Employee_Name'], var_name='Material_Name', value_name='Quantity')
    df_melted['Quantity'] = df_melted['Quantity'].apply(clean_quantity)
    df_melted = df_melted[df_melted['Quantity'] > 0].dropna(subset=['Employee_Name', 'Material_Name'])
    df_melted = df_melted[~df_melted['Employee_Name'].astype(str).str.contains('เดือน')]
    
    return df_melted.to_dict('records')

def run_etl_pipeline(requisitions_file, purchases_file):
    logger.info("Starting Multi-threaded ETL Pipeline...")
    
    # 1. Process Requisitions
    all_transactions = []
    if requisitions_file:
        logger.info(f"Reading {requisitions_file}")
        xls_req = pd.ExcelFile(requisitions_file)
        
        # CPU Acceleration: Process sheets in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_requisition_sheet, xls_req, sheet): sheet for sheet in xls_req.sheet_names}
            for future in concurrent.futures.as_completed(futures):
                all_transactions.extend(future.result())
                
        # Map IDs and prepare for batch insert
        mapped_transactions = []
        for row in all_transactions:
            emp_id = get_or_create_employee(row['Employee_Name'])
            mat_id = get_or_create_material(row['Material_Name'])
            mapped_transactions.append({
                "employee_id": emp_id,
                "material_id": mat_id,
                "quantity": row['Quantity']
            })
        batch_insert("transactions", mapped_transactions)

    # 2. Process Purchases (Synchronous is fine here as it's usually smaller, but can be threaded too)
    if purchases_file:
        logger.info(f"Reading {purchases_file}")
        xls_pur = pd.ExcelFile(purchases_file)
        mapped_purchases = []
        
        for sheet_name in xls_pur.sheet_names:
            if "สรุปยอด" in sheet_name:
                continue
            df = pd.read_excel(xls_pur, sheet_name=sheet_name)
            col_map = {'รายการ': 'Material_Name', 'ชื่อร้าน': 'Supplier_Name', 'จำนวน': 'Quantity', 'ราคา/ชิ้น': 'Price_Per_Unit', 'รวมจำนวนเงิน': 'Total_Amount', 'ว/ด/ป': 'Purchase_Date'}
            df.rename(columns=col_map, inplace=True)
            df = df[[c for c in col_map.values() if c in df.columns]].dropna(subset=['Material_Name', 'Total_Amount'])
            
            if 'Quantity' in df.columns:
                df['Quantity'] = df['Quantity'].apply(clean_quantity)
                
            for _, row in df.iterrows():
                mat_id = get_or_create_material(row['Material_Name'])
                clean_dt = fix_thai_date(row.get('Purchase_Date'))
                mapped_purchases.append({
                    "material_id": mat_id,
                    "supplier_name": str(row.get('Supplier_Name', '')),
                    "quantity": row.get('Quantity', 0),
                    "price_per_unit": row.get('Price_Per_Unit', 0),
                    "total_amount": row.get('Total_Amount', 0),
                    "purchase_date": clean_dt.strftime('%Y-%m-%d') if clean_dt else None
                })
        batch_insert("purchases", mapped_purchases)
        logger.info("ETL Pipeline Completed Successfully.")