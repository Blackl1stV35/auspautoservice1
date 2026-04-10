"""
SP Auto Service - ระบบจัดการวัสดุสิ้นเปลือง Phase 1
อู่เอสพี ออโต้เซอร์วิส จ.ฉะเชิงเทรา
"""
import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.etl import run_full_etl, DATA_DIR
from src import data_store as ds

st.set_page_config(
    page_title="SP Auto Service - ระบบวัสดุ",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for mobile-friendly Thai UI ---
st.markdown("""
<style>
    .big-btn button { font-size: 1.3rem !important; padding: 0.8rem 2rem !important; }
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        font-size: 1.1rem !important; font-weight: 600 !important;
    }
    div[data-testid="stMetric"] {
        background: #f8f9fa; border-radius: 10px; padding: 12px; border-left: 4px solid #FF6B35;
    }
    .success-box { background: #d4edda; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
                   border-left: 4px solid #28a745; font-size: 1.1rem; }
    .warn-box { background: #fff3cd; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
                border-left: 4px solid #ffc107; }
</style>
""", unsafe_allow_html=True)


def load_data():
    """Load all CSVs into session state."""
    for name in ["requisitions", "employees", "materials", "stock", "purchases", "audit_log"]:
        st.session_state[name] = ds.load(name)


# Initialize
if "initialized" not in st.session_state:
    load_data()
    st.session_state.initialized = True

# --- Sidebar Navigation ---
st.sidebar.image("https://img.icons8.com/color/96/car-service.png", width=64)
st.sidebar.title("🔧 SP Auto Service")
st.sidebar.caption("ระบบจัดการวัสดุสิ้นเปลือง v1.0")

page = st.sidebar.radio("เมนู", [
    "🏠 หน้าหลัก",
    "📤 อัปโหลด Excel",
    "📝 เบิกวัสดุ",
    "📦 สต็อกวัสดุ",
    "📊 รายงานช่าง",
    "⚠️ ตรวจจับความผิดปกติ",
    "🔍 ประวัติการใช้งาน",
], index=0)

st.sidebar.divider()
st.sidebar.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ============================================================
# PAGE: หน้าหลัก
# ============================================================
if page == "🏠 หน้าหลัก":
    st.title("🏠 ภาพรวมระบบ")
    st.markdown("**อู่เอสพี ออโต้เซอร์วิส** — ระบบจัดการวัสดุสิ้นเปลือง")

    req = st.session_state.get("requisitions", pd.DataFrame())
    emp = st.session_state.get("employees", pd.DataFrame())
    mat = st.session_state.get("materials", pd.DataFrame())
    stock = st.session_state.get("stock", pd.DataFrame())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👷 จำนวนช่าง", len(emp) if not emp.empty else 0)
    c2.metric("🧰 รายการวัสดุ", len(mat) if not mat.empty else 0)
    c3.metric("📋 รายการเบิก", len(req) if not req.empty else 0)

    low_stock = ds.get_low_stock()
    c4.metric("⚠️ วัสดุใกล้หมด", len(low_stock) if not low_stock.empty else 0)

    if not req.empty and "material_name" in req.columns:
        st.subheader("🏆 วัสดุที่เบิกมากที่สุด (Top 10)")
        req["quantity"] = pd.to_numeric(req["quantity"], errors="coerce").fillna(0)
        top = req.groupby("material_name")["quantity"].sum().nlargest(10).reset_index()
        fig = px.bar(top, x="quantity", y="material_name", orientation="h",
                     color="quantity", color_continuous_scale="Oranges",
                     labels={"quantity": "จำนวนรวม", "material_name": "วัสดุ"})
        fig.update_layout(yaxis=dict(autorange="reversed"), height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    if not low_stock.empty:
        st.subheader("⚠️ วัสดุใกล้หมด")
        st.dataframe(low_stock[["item_name", "current_qty"]].rename(
            columns={"item_name": "วัสดุ", "current_qty": "คงเหลือ"}
        ), use_container_width=True, hide_index=True)


# ============================================================
# PAGE: อัปโหลด Excel
# ============================================================
elif page == "📤 อัปโหลด Excel":
    st.title("📤 อัปโหลดไฟล์ Excel")
    st.info("อัปโหลดไฟล์ Excel 2 ไฟล์จากระบบเดิม แล้วกดประมวลผล")

    col1, col2 = st.columns(2)
    with col1:
        req_file = st.file_uploader("📄 ไฟล์เบิกวัสดุสิ้นเปลือง", type=["xlsx", "xls"],
                                     key="req_upload")
    with col2:
        pur_file = st.file_uploader("📄 ไฟล์ต้นทุน/สั่งซื้อ", type=["xlsx", "xls"],
                                     key="pur_upload")

    if st.button("🚀 ประมวลผล ETL", type="primary", use_container_width=True):
        if not req_file and not pur_file:
            st.error("กรุณาอัปโหลดไฟล์อย่างน้อย 1 ไฟล์")
        else:
            os.makedirs(DATA_DIR, exist_ok=True)
            req_path = pur_path = None

            if req_file:
                req_path = os.path.join(DATA_DIR, "upload_requisitions.xlsx")
                with open(req_path, "wb") as f:
                    f.write(req_file.read())

            if pur_file:
                pur_path = os.path.join(DATA_DIR, "upload_purchases.xlsx")
                with open(pur_path, "wb") as f:
                    f.write(pur_file.read())

            with st.spinner("⏳ กำลังประมวลผล... อาจใช้เวลาสักครู่"):
                try:
                    result = run_full_etl(req_path, pur_path)
                    load_data()
                    ds.log_audit("admin", "ETL", f"อัปโหลดไฟล์ req={bool(req_file)} pur={bool(pur_file)}")
                    ds.git_commit("ETL: อัปโหลดไฟล์ Excel ใหม่")

                    st.markdown('<div class="success-box">✅ ประมวลผลสำเร็จ!</div>',
                                unsafe_allow_html=True)

                    for key, label in [
                        ("requisitions", "รายการเบิก"),
                        ("employees", "รายชื่อช่าง"),
                        ("materials", "รายการวัสดุ"),
                        ("purchases", "รายการซื้อ"),
                    ]:
                        if key in result and not result[key].empty:
                            st.success(f"📊 {label}: {len(result[key])} รายการ")
                except Exception as e:
                    st.error(f"❌ เกิดข้อผิดพลาด: {e}")


# ============================================================
# PAGE: เบิกวัสดุ
# ============================================================
elif page == "📝 เบิกวัสดุ":
    st.title("📝 ฟอร์มเบิกวัสดุ")

    emp = st.session_state.get("employees", pd.DataFrame())
    mat = st.session_state.get("materials", pd.DataFrame())

    if emp.empty or mat.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลช่าง/วัสดุ กรุณาอัปโหลด Excel ก่อน")
    else:
        emp_names = sorted(emp["name"].dropna().unique().tolist())
        mat_names = sorted(mat["item_name"].dropna().unique().tolist())

        st.markdown("### เลือกรายการเบิก")
        col1, col2 = st.columns(2)
        with col1:
            selected_emp = st.selectbox("👷 ชื่อช่าง", emp_names, index=0)
        with col2:
            selected_mat = st.selectbox("🧰 วัสดุ", mat_names, index=0)

        quantity = st.number_input("📦 จำนวน", min_value=1, max_value=100, value=1, step=1)
        issued_by = st.text_input("🔑 ผู้บันทึก", value="admin")

        st.divider()
        st.markdown(f"**สรุป:** {selected_emp} เบิก **{selected_mat}** จำนวน **{quantity}** ชิ้น")

        if st.button("✅ ยืนยันเบิกวัสดุ", type="primary", use_container_width=True):
            try:
                ds.issue_material(selected_emp, selected_mat, quantity, issued_by)
                load_data()
                st.markdown(
                    f'<div class="success-box">✅ บันทึกสำเร็จ! {selected_emp} เบิก {selected_mat} x{quantity}</div>',
                    unsafe_allow_html=True
                )
                st.balloons()
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {e}")


# ============================================================
# PAGE: สต็อกวัสดุ
# ============================================================
elif page == "📦 สต็อกวัสดุ":
    st.title("📦 สต็อกวัสดุปัจจุบัน")

    stock = st.session_state.get("stock", pd.DataFrame())
    if stock.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลสต็อก")
    else:
        stock["current_qty"] = pd.to_numeric(stock["current_qty"], errors="coerce").fillna(0).astype(int)
        search = st.text_input("🔍 ค้นหาวัสดุ", "")
        display = stock.copy()
        if search:
            display = display[display["item_name"].str.contains(search, case=False, na=False)]

        # Color-code low stock
        def highlight_low(row):
            if row["current_qty"] <= 5:
                return ["background-color: #f8d7da"] * len(row)
            if row["current_qty"] <= 10:
                return ["background-color: #fff3cd"] * len(row)
            return [""] * len(row)

        st.dataframe(
            display[["item_name", "current_qty", "last_updated"]].rename(columns={
                "item_name": "วัสดุ", "current_qty": "คงเหลือ", "last_updated": "อัปเดตล่าสุด"
            }).style.apply(highlight_low, axis=1),
            use_container_width=True, hide_index=True, height=500
        )

        st.divider()
        st.subheader("➕ รับวัสดุเข้าสต็อก")
        c1, c2, c3 = st.columns(3)
        mat_names = sorted(stock["item_name"].dropna().unique().tolist())
        with c1:
            add_mat = st.selectbox("วัสดุ", mat_names, key="add_stock_mat")
        with c2:
            add_qty = st.number_input("จำนวน", min_value=1, value=10, key="add_stock_qty")
        with c3:
            add_user = st.text_input("ผู้รับเข้า", value="admin", key="add_stock_user")
        if st.button("✅ รับเข้าสต็อก", type="primary"):
            ds.add_stock(add_mat, add_qty, add_user)
            load_data()
            st.success(f"✅ รับเข้า {add_mat} +{add_qty}")
            st.rerun()


# ============================================================
# PAGE: รายงานช่าง
# ============================================================
elif page == "📊 รายงานช่าง":
    st.title("📊 รายงานการเบิกวัสดุรายช่าง")

    req = st.session_state.get("requisitions", pd.DataFrame())
    if req.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลการเบิก")
    else:
        req["quantity"] = pd.to_numeric(req["quantity"], errors="coerce").fillna(0)
        emp_names = sorted(req["employee_name"].dropna().unique().tolist())

        view_mode = st.radio("มุมมอง", ["ภาพรวมทุกคน", "รายบุคคล"], horizontal=True)

        if view_mode == "ภาพรวมทุกคน":
            usage = req.groupby("employee_name")["quantity"].sum().sort_values(ascending=False).reset_index()
            usage.columns = ["ชื่อช่าง", "จำนวนเบิกรวม"]
            st.dataframe(usage, use_container_width=True, hide_index=True)

            fig = px.bar(usage.head(15), x="ชื่อช่าง", y="จำนวนเบิกรวม",
                         color="จำนวนเบิกรวม", color_continuous_scale="Reds")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            selected = st.selectbox("เลือกช่าง", emp_names)
            emp_req = req[req["employee_name"] == selected]
            by_mat = emp_req.groupby("material_name")["quantity"].sum().sort_values(ascending=False).reset_index()
            by_mat.columns = ["วัสดุ", "จำนวน"]
            st.metric("จำนวนเบิกทั้งหมด", int(by_mat["จำนวน"].sum()))
            st.dataframe(by_mat, use_container_width=True, hide_index=True)

            fig = px.pie(by_mat.head(10), values="จำนวน", names="วัสดุ",
                         title=f"สัดส่วนวัสดุที่ {selected} เบิก")
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE: ตรวจจับความผิดปกติ
# ============================================================
elif page == "⚠️ ตรวจจับความผิดปกติ":
    st.title("⚠️ ตรวจจับการเบิกผิดปกติ")
    st.info("ระบบจะแจ้งเตือนช่างที่เบิกวัสดุมากผิดปกติ (มากกว่า 2 เท่าของค่าเบี่ยงเบนมาตรฐาน)")

    threshold = st.slider("ค่า Z-Score Threshold", 1.0, 4.0, 2.0, 0.5)
    anomalies = ds.get_anomalies(threshold)

    if anomalies.empty:
        st.success("✅ ไม่พบความผิดปกติ")
    else:
        st.warning(f"🚨 พบ {len(anomalies)} รายการที่น่าสงสัย")
        anomalies.columns = ["ชื่อช่าง", "จำนวนเบิกรวม", "Z-Score"]
        anomalies["Z-Score"] = anomalies["Z-Score"].round(2)
        st.dataframe(anomalies, use_container_width=True, hide_index=True)

        # Compare all employees
        req = st.session_state.get("requisitions", pd.DataFrame())
        if not req.empty:
            req["quantity"] = pd.to_numeric(req["quantity"], errors="coerce").fillna(0)
            all_usage = req.groupby("employee_name")["quantity"].sum().sort_values(ascending=False).reset_index()
            mean_val = all_usage["quantity"].mean()
            fig = px.bar(all_usage, x="employee_name", y="quantity",
                         labels={"employee_name": "ช่าง", "quantity": "จำนวนเบิกรวม"})
            fig.add_hline(y=mean_val, line_dash="dash", line_color="red",
                          annotation_text=f"ค่าเฉลี่ย ({mean_val:.0f})")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE: ประวัติการใช้งาน (Audit Log)
# ============================================================
elif page == "🔍 ประวัติการใช้งาน":
    st.title("🔍 ประวัติการใช้งานระบบ")

    audit = ds.load("audit_log")
    if audit.empty:
        st.info("ยังไม่มีประวัติการใช้งาน")
    else:
        audit = audit.sort_values("timestamp", ascending=False).head(100)
        audit.columns = ["เวลา", "ผู้ใช้", "การกระทำ", "รายละเอียด"]
        st.dataframe(audit, use_container_width=True, hide_index=True, height=600)

    # Also show purchases if available
    pur = st.session_state.get("purchases", pd.DataFrame())
    if not pur.empty:
        with st.expander("📋 ประวัติการสั่งซื้อ (จาก Excel)"):
            cols = [c for c in ["item_name", "supplier_name", "quantity", "total_amount",
                                 "purchase_date", "sheet_category"] if c in pur.columns]
            display_pur = pur[cols].copy()
            display_pur.columns = [{"item_name": "รายการ", "supplier_name": "ร้านค้า",
                                     "quantity": "จำนวน", "total_amount": "ยอดรวม",
                                     "purchase_date": "วันที่", "sheet_category": "หมวด"}.get(c, c)
                                    for c in cols]
            st.dataframe(display_pur, use_container_width=True, hide_index=True, height=400)
