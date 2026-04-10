"""
SP Auto Service - ระบบจัดการวัสดุสิ้นเปลือง Phase 1
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from src import data_store as ds

st.set_page_config(page_title="SP Auto Service", layout="wide")

st.title("🚗 SP Auto Service - ระบบจัดการวัสดุสิ้นเปลือง")

# Load data
stock_df = ds.add_stock()
req_df = ds.get_requisitions()

# Sidebar
st.sidebar.title("เมนู")
page = st.sidebar.radio("เลือกหน้า", [
    "🏠 หน้าหลัก",
    "📝 เบิกวัสดุ",
    "📦 สต็อกวัสดุ",
    "📊 รายงานการเบิก",
    "📤 อัปโหลด Excel"
])

# ====================== PAGES ======================
if page == "🏠 หน้าหลัก":
    st.header("ภาพรวมระบบ")
    col1, col2, col3 = st.columns(3)
    col1.metric("วัสดุทั้งหมด", len(stock_df))
    col2.metric("การเบิกทั้งหมด", len(req_df))
    low = len(stock_df[stock_df.get('quantity', 0) <= 5]) if not stock_df.empty else 0
    col3.metric("วัสดุใกล้หมด", low)

elif page == "📝 เบิกวัสดุ":
    st.header("เบิกวัสดุ")
    if stock_df.empty:
        st.warning("ยังไม่มีข้อมูลวัสดุ")
    else:
        mechanics = ["บุญมา(กล้า)", "ชาญชัย(โจ้)", "ชุลีพร(ถิง)", "อื่นๆ"]
        mechanic = st.selectbox("ชื่อช่าง", mechanics)
        material = st.selectbox("วัสดุ", stock_df.get("material_name", stock_df.get("item_name", [])).tolist())
        quantity = st.number_input("จำนวน", min_value=0.1, value=1.0, step=0.5)
        
        if st.button("ยืนยันการเบิก", type="primary"):
            ds.save_requisition(mechanic, material, quantity)
            st.success(f"เบิก {quantity} {material} ให้ {mechanic} สำเร็จ")
            st.rerun()

elif page == "📦 สต็อกวัสดุ":
    st.header("สต็อกวัสดุปัจจุบัน")
    if stock_df.empty:
        st.warning("ยังไม่มีข้อมูลสต็อก")
    else:
        qty_col = "current_qty" if "current_qty" in stock_df.columns else "quantity"
        display = stock_df.copy()
        
        def highlight(row):
            if row.get(qty_col, 0) <= 5:
                return ['background-color: #ffe6e6'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            display.style.apply(highlight, axis=1),
            use_container_width=True,
            hide_index=True
        )

elif page == "📊 รายงานการเบิก":
    st.header("รายงานการเบิก")
    if req_df.empty:
        st.info("ยังไม่มีรายการเบิก")
    else:
        req_df["quantity"] = pd.to_numeric(req_df["quantity"], errors="coerce").fillna(0)
        summary = req_df.groupby("mechanic")["quantity"].sum().reset_index()
        st.dataframe(summary, use_container_width=True, hide_index=True)

elif page == "📤 อัปโหลด Excel":
    st.header("อัปโหลดไฟล์ Excel")
    st.info("ฟีเจอร์นี้จะพัฒนาเต็มรูปแบบใน Phase 2")

st.caption("SP Auto Service Phase 1 | April 2026")