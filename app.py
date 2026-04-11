"""
SP Auto Service - ระบบจัดการวัสดุสิ้นเปลือง Phase 1 (Enhanced)
อู่เอสพี ออโต้เซอร์วิส จ.ฉะเชิงเทรา

Enhancements over v1:
  • Monthly vs cumulative dashboard views (VBA "N+" style)
  • Usage-intensity heatmap (employee × material)
  • Top-10 materials & top mechanics charts on home
  • Tiered stock alerts with 🔴🟠🟡🟢 status
  • UUID transaction IDs + duplicate prevention
  • Per-material anomaly detection
"""
import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.etl import run_full_etl, DATA_DIR
from src import data_store as ds

# ─── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="SP Auto Service - ระบบวัสดุ",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Mobile-friendly sizing */
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        font-size: 1.1rem !important; font-weight: 600 !important;
    }
    div[data-testid="stMetric"] {
        background: #f8f9fa; border-radius: 10px; padding: 12px;
        border-left: 4px solid #FF6B35;
    }
    .success-box {
        background: #d4edda; padding: 1rem; border-radius: 8px;
        margin: 0.5rem 0; border-left: 4px solid #28a745; font-size: 1.1rem;
    }
    .dup-box {
        background: #fff3cd; padding: 1rem; border-radius: 8px;
        margin: 0.5rem 0; border-left: 4px solid #ffc107; font-size: 1.1rem;
    }
    .tx-id { color: #6c757d; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)


# ─── Data refresh helper ─────────────────────────────────────────
def refresh_data():
    st.session_state["requisitions"] = ds.get_requisitions()
    st.session_state["employees"]    = ds.get_employees()
    st.session_state["materials"]    = ds.get_materials()
    st.session_state["stock"]        = ds.get_stock()
    st.session_state["purchases"]    = ds.get_purchases()
    st.session_state["audit_log"]    = ds.get_audit_log()


if "initialized" not in st.session_state:
    refresh_data()
    st.session_state["initialized"] = True


# ─── Sidebar ─────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/car-service.png", width=64)
st.sidebar.title("🔧 SP Auto Service")
st.sidebar.caption("ระบบจัดการวัสดุสิ้นเปลือง v2.0")

page = st.sidebar.radio("เมนู", [
    "🏠 หน้าหลัก",
    "📤 อัปโหลด Excel",
    "📝 เบิกวัสดุ",
    "📦 สต็อกวัสดุ",
    "📊 รายงานช่าง",
    "🗓️ สรุปรายเดือน",
    "🔥 Heatmap การใช้งาน",
    "⚠️ ตรวจจับความผิดปกติ",
    "🔍 ประวัติการใช้งาน",
], index=0)

st.sidebar.divider()
st.sidebar.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")


# ═══════════════════════════════════════════════════════════════════
# 🏠 หน้าหลัก — Enhanced with top mechanics + materials side-by-side
# ═══════════════════════════════════════════════════════════════════
if page == "🏠 หน้าหลัก":
    st.title("🏠 ภาพรวมระบบ")
    st.markdown("**อู่เอสพี ออโต้เซอร์วิส** — ระบบจัดการวัสดุสิ้นเปลือง")

    req   = st.session_state["requisitions"]
    emp   = st.session_state["employees"]
    mat   = st.session_state["materials"]
    stock = st.session_state["stock"]
    low   = ds.get_low_stock()

    # ── KPI row ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👷 จำนวนช่าง",    len(emp)  if not emp.empty  else 0)
    c2.metric("🧰 รายการวัสดุ",  len(mat)  if not mat.empty  else 0)
    c3.metric("📋 รายการเบิก",   len(req)  if not req.empty  else 0)
    c4.metric("⚠️ วัสดุใกล้หมด", len(low)  if not low.empty  else 0)

    if not req.empty and "material_name" in req.columns:
        # ── Top-10 materials + Top-10 mechanics side by side ──
        st.divider()
        left, right = st.columns(2)

        with left:
            st.subheader("🏆 Top 10 วัสดุ")
            top_mat = (req.groupby("material_name")["quantity"]
                          .sum().nlargest(10).reset_index())
            fig_m = px.bar(top_mat, x="quantity", y="material_name",
                           orientation="h", color="quantity",
                           color_continuous_scale="Oranges",
                           labels={"quantity": "จำนวน", "material_name": "วัสดุ"})
            fig_m.update_layout(yaxis=dict(autorange="reversed"),
                                height=380, showlegend=False,
                                margin=dict(l=0, r=10, t=10, b=0))
            st.plotly_chart(fig_m, use_container_width=True)

        with right:
            st.subheader("👷 Top 10 ช่าง")
            top_emp = (req.groupby("employee_name")["quantity"]
                          .sum().nlargest(10).reset_index())
            fig_e = px.bar(top_emp, x="quantity", y="employee_name",
                           orientation="h", color="quantity",
                           color_continuous_scale="Blues",
                           labels={"quantity": "จำนวน", "employee_name": "ช่าง"})
            fig_e.update_layout(yaxis=dict(autorange="reversed"),
                                height=380, showlegend=False,
                                margin=dict(l=0, r=10, t=10, b=0))
            st.plotly_chart(fig_e, use_container_width=True)

    # ── Low stock alerts with status badges ──
    if not low.empty:
        st.subheader("⚠️ วัสดุใกล้หมด")
        low_display = low[["item_name", "current_qty"]].copy()
        low_display["สถานะ"] = low_display["current_qty"].apply(ds.get_stock_status)
        low_display.rename(columns={"item_name": "วัสดุ", "current_qty": "คงเหลือ"},
                           inplace=True)
        st.dataframe(low_display, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# 📤 อัปโหลด Excel
# ═══════════════════════════════════════════════════════════════════
elif page == "📤 อัปโหลด Excel":
    st.title("📤 อัปโหลดไฟล์ Excel")
    st.info("อัปโหลดไฟล์ Excel 2 ไฟล์จากระบบเดิม แล้วกดประมวลผล")

    col1, col2 = st.columns(2)
    with col1:
        req_file = st.file_uploader("📄 ไฟล์เบิกวัสดุสิ้นเปลือง",
                                     type=["xlsx", "xls"], key="req_upload")
    with col2:
        pur_file = st.file_uploader("📄 ไฟล์ต้นทุน/สั่งซื้อ",
                                     type=["xlsx", "xls"], key="pur_upload")

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

            with st.spinner("⏳ กำลังประมวลผล..."):
                try:
                    result = run_full_etl(req_path, pur_path)  # auto-commits internally
                    refresh_data()
                    ds.log_audit("admin", "ETL",
                                 f"อัปโหลด req={bool(req_file)} pur={bool(pur_file)}",
                                 commit=True)  # commit the audit entry too
                    st.markdown('<div class="success-box">✅ ประมวลผลสำเร็จ!</div>',
                                unsafe_allow_html=True)
                    for key, label in [("requisitions", "รายการเบิก"),
                                       ("employees", "รายชื่อช่าง"),
                                       ("materials", "รายการวัสดุ"),
                                       ("purchases", "รายการซื้อ")]:
                        if key in result and not result[key].empty:
                            st.success(f"📊 {label}: {len(result[key])} รายการ")
                    st.caption("💾 บันทึกลง Git แล้ว")
                except Exception as e:
                    st.error(f"❌ เกิดข้อผิดพลาด: {e}")


# ═══════════════════════════════════════════════════════════════════
# 📝 เบิกวัสดุ — with duplicate prevention + tx ID feedback
# ═══════════════════════════════════════════════════════════════════
elif page == "📝 เบิกวัสดุ":
    st.title("📝 ฟอร์มเบิกวัสดุ")

    emp = st.session_state["employees"]
    mat = st.session_state["materials"]

    if emp.empty or mat.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลช่าง/วัสดุ กรุณาอัปโหลด Excel ก่อน")
    else:
        emp_names = sorted(emp["name"].dropna().unique().tolist())
        mat_names = sorted(mat["item_name"].dropna().unique().tolist())

        st.markdown("### เลือกรายการเบิก")
        col1, col2 = st.columns(2)
        with col1:
            selected_emp = st.selectbox("👷 ชื่อช่าง", emp_names)
        with col2:
            selected_mat = st.selectbox("🧰 วัสดุ", mat_names)

        quantity  = st.number_input("📦 จำนวน", min_value=1, max_value=100,
                                    value=1, step=1)
        issued_by = st.text_input("🔑 ผู้บันทึก", value="admin")

        # Show current stock for this material
        stock = st.session_state["stock"]
        if not stock.empty and "item_name" in stock.columns:
            mat_stock = stock[stock["item_name"] == selected_mat]
            if not mat_stock.empty:
                curr = int(mat_stock.iloc[0].get("current_qty", 0))
                status = ds.get_stock_status(curr)
                st.info(f"📦 สต็อกปัจจุบัน: **{selected_mat}** = **{curr}** ชิ้น {status}")

        st.divider()
        st.markdown(
            f"**สรุป:** {selected_emp} เบิก "
            f"**{selected_mat}** จำนวน **{quantity}** ชิ้น")

        if st.button("✅ ยืนยันเบิกวัสดุ", type="primary",
                     use_container_width=True):
            result = ds.issue_material(selected_emp, selected_mat,
                                       quantity, issued_by)
            if result["ok"]:
                refresh_data()
                git_icon = "💾" if result.get("committed") else "⚠️"
                git_text = ("บันทึกลง Git แล้ว" if result.get("committed")
                            else "ข้อมูลบันทึกแล้ว แต่ Git commit ไม่สำเร็จ")
                st.markdown(
                    f'<div class="success-box">{result["msg"]}</div>'
                    f'<div class="tx-id">🔖 รหัส: {result["tx_id"]}  '
                    f'{git_icon} {git_text}</div>',
                    unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(
                    f'<div class="dup-box">{result["msg"]}</div>',
                    unsafe_allow_html=True)

        # ── Recent issuances ──
        req = st.session_state["requisitions"]
        if not req.empty:
            with st.expander("📋 รายการเบิกล่าสุด (20 รายการ)"):
                recent_cols = [c for c in ["tx_id", "date", "time",
                                            "employee_name", "material_name",
                                            "quantity", "issued_by"]
                               if c in req.columns]
                recent = req[recent_cols].tail(20).iloc[::-1]
                rename = {"tx_id": "รหัส", "date": "วันที่", "time": "เวลา",
                          "employee_name": "ช่าง", "material_name": "วัสดุ",
                          "quantity": "จำนวน", "issued_by": "ผู้บันทึก"}
                st.dataframe(recent.rename(columns=rename),
                             use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# 📦 สต็อกวัสดุ — tiered color + status badges
# ═══════════════════════════════════════════════════════════════════
elif page == "📦 สต็อกวัสดุ":
    st.title("📦 สต็อกวัสดุปัจจุบัน")

    stock = st.session_state["stock"]
    if stock.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลสต็อก")
    else:
        search = st.text_input("🔍 ค้นหาวัสดุ", "")
        display = stock.copy()
        if search:
            display = display[
                display["item_name"].str.contains(search, case=False, na=False)]

        # Add status column BEFORE rename
        display["status"] = display["current_qty"].apply(ds.get_stock_status)

        cols_show = [c for c in ["item_name", "current_qty", "status", "last_updated"]
                     if c in display.columns]
        rename_map = {"item_name": "วัสดุ", "current_qty": "คงเหลือ",
                      "status": "สถานะ", "last_updated": "อัปเดตล่าสุด"}
        styled_df = display[cols_show].rename(columns=rename_map)

        # Tiered row coloring (operates on renamed columns)
        def highlight_stock(row):
            qty = 99
            try:
                qty = int(row.get("คงเหลือ", 99))
            except (ValueError, TypeError):
                pass
            if qty <= 0:
                return ["background-color: #f5c6cb"] * len(row)
            if qty <= 5:
                return ["background-color: #f8d7da"] * len(row)
            if qty <= 10:
                return ["background-color: #fff3cd"] * len(row)
            return [""] * len(row)

        st.dataframe(
            styled_df.style.apply(highlight_stock, axis=1),
            use_container_width=True, hide_index=True, height=500)

        # ── Stock distribution chart ──
        if len(display) > 0:
            status_counts = display["status"].value_counts().reset_index()
            status_counts.columns = ["สถานะ", "จำนวน"]
            fig = px.pie(status_counts, values="จำนวน", names="สถานะ",
                         color="สถานะ",
                         color_discrete_map={
                             "🔴 หมด": "#dc3545", "🟠 วิกฤต": "#fd7e14",
                             "🟡 ต่ำ": "#ffc107", "🟢 ปกติ": "#28a745"},
                         title="สัดส่วนสถานะสต็อก")
            st.plotly_chart(fig, use_container_width=True)

        # ── Receive stock sub-form ──
        st.divider()
        st.subheader("➕ รับวัสดุเข้าสต็อก")
        c1, c2, c3 = st.columns(3)
        mat_names = sorted(stock["item_name"].dropna().unique().tolist())
        with c1:
            add_mat = st.selectbox("วัสดุ", mat_names, key="add_stock_mat")
        with c2:
            add_qty = st.number_input("จำนวน", min_value=1, value=10,
                                      key="add_stock_qty")
        with c3:
            add_user = st.text_input("ผู้รับเข้า", value="admin",
                                     key="add_stock_user")
        if st.button("✅ รับเข้าสต็อก", type="primary"):
            result = ds.add_stock(add_mat, add_qty, add_user)
            refresh_data()
            if result and result.get("ok"):
                git_icon = "💾" if result.get("committed") else "⚠️"
                st.success(f"{result['msg']}  {git_icon}")
            else:
                st.warning(result.get("msg", "ไม่สามารถเพิ่มสต็อกได้"))
            st.rerun()


# ═══════════════════════════════════════════════════════════════════
# 📊 รายงานช่าง — monthly vs cumulative toggle
# ═══════════════════════════════════════════════════════════════════
elif page == "📊 รายงานช่าง":
    st.title("📊 รายงานการเบิกวัสดุรายช่าง")

    req = st.session_state["requisitions"]
    if req.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลการเบิก")
    else:
        emp_names = sorted(req["employee_name"].dropna().unique().tolist())

        # ── View mode selector ──
        view_mode = st.radio("มุมมอง",
                             ["ภาพรวมทุกคน (สะสม)", "เปรียบเทียบรายเดือน", "รายบุคคล"],
                             horizontal=True)

        if view_mode == "ภาพรวมทุกคน (สะสม)":
            usage = (req.groupby("employee_name")["quantity"]
                        .sum().sort_values(ascending=False).reset_index())
            usage.columns = ["ชื่อช่าง", "จำนวนเบิกรวม"]
            st.dataframe(usage, use_container_width=True, hide_index=True)
            fig = px.bar(usage.head(15), x="ชื่อช่าง", y="จำนวนเบิกรวม",
                         color="จำนวนเบิกรวม", color_continuous_scale="Reds")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        elif view_mode == "เปรียบเทียบรายเดือน":
            # Monthly comparison — grouped bar chart
            periods = ds.get_available_periods()
            if not periods:
                st.info("ไม่มีข้อมูลรายเดือน")
            else:
                req_copy = req.copy()
                req_copy["period"] = req_copy.apply(
                    lambda r: f"{int(r['month']):02d}/{int(r['year'])}"
                    if pd.notna(r.get("month")) and pd.notna(r.get("year"))
                    else None, axis=1)
                monthly = (req_copy.groupby(["employee_name", "period"])["quantity"]
                                   .sum().reset_index())
                fig = px.bar(monthly, x="employee_name", y="quantity",
                             color="period", barmode="group",
                             labels={"employee_name": "ช่าง", "quantity": "จำนวน",
                                     "period": "เดือน/ปี"})
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("📋 ตารางสะสมรายเดือน (แบบ VBA)")
                monthly_pivot = ds.get_monthly_summary()
                if not monthly_pivot.empty:
                    st.dataframe(monthly_pivot, use_container_width=True)

        else:  # รายบุคคล
            selected = st.selectbox("เลือกช่าง", emp_names)
            emp_req = req[req["employee_name"] == selected]
            by_mat = (emp_req.groupby("material_name")["quantity"]
                             .sum().sort_values(ascending=False).reset_index())
            by_mat.columns = ["วัสดุ", "จำนวน"]

            c1, c2 = st.columns(2)
            c1.metric("จำนวนเบิกทั้งหมด", int(by_mat["จำนวน"].sum()))
            c2.metric("จำนวนรายการวัสดุ", len(by_mat))

            st.dataframe(by_mat, use_container_width=True, hide_index=True)
            fig = px.pie(by_mat.head(10), values="จำนวน", names="วัสดุ",
                         title=f"สัดส่วนวัสดุที่ {selected} เบิก")
            st.plotly_chart(fig, use_container_width=True)

            # Monthly breakdown for this employee
            if "month" in emp_req.columns and "year" in emp_req.columns:
                emp_req_c = emp_req.copy()
                emp_req_c["period"] = emp_req_c.apply(
                    lambda r: f"{int(r['month']):02d}/{int(r['year'])}"
                    if pd.notna(r.get("month")) else None, axis=1)
                monthly = (emp_req_c.groupby("period")["quantity"]
                                    .sum().reset_index())
                if len(monthly) > 1:
                    st.subheader("📈 แนวโน้มรายเดือน")
                    fig2 = px.line(monthly, x="period", y="quantity",
                                   markers=True,
                                   labels={"period": "เดือน", "quantity": "จำนวน"})
                    st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# 🗓️ สรุปรายเดือน — VBA monthly sheet accumulation
# ═══════════════════════════════════════════════════════════════════
elif page == "🗓️ สรุปรายเดือน":
    st.title("🗓️ สรุปการเบิกรายเดือน")
    st.info("แสดงยอดสะสมรายเดือนแบบเดียวกับชีท VBA เดิม")

    tab1, tab2 = st.tabs(["👷 รายช่าง × เดือน", "🧰 รายวัสดุ × เดือน"])

    with tab1:
        pivot_emp = ds.get_monthly_summary()
        if pivot_emp.empty:
            st.warning("ยังไม่มีข้อมูล")
        else:
            st.dataframe(pivot_emp, use_container_width=True, height=500)

            st.subheader("📊 กราฟเปรียบเทียบยอดรวม")
            totals = pivot_emp["รวมทั้งหมด"].reset_index()
            totals.columns = ["ช่าง", "รวม"]
            fig = px.bar(totals.sort_values("รวม", ascending=False).head(15),
                         x="ช่าง", y="รวม", color="รวม",
                         color_continuous_scale="Reds")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        pivot_mat = ds.get_monthly_by_material()
        if pivot_mat.empty:
            st.warning("ยังไม่มีข้อมูล")
        else:
            st.dataframe(pivot_mat, use_container_width=True, height=500)

            st.subheader("📊 กราฟเปรียบเทียบยอดรวม")
            totals = pivot_mat["รวมทั้งหมด"].reset_index()
            totals.columns = ["วัสดุ", "รวม"]
            fig = px.bar(totals.sort_values("รวม", ascending=False).head(15),
                         x="วัสดุ", y="รวม", color="รวม",
                         color_continuous_scale="Oranges")
            st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# 🔥 Heatmap — usage intensity (employee × material)
# ═══════════════════════════════════════════════════════════════════
elif page == "🔥 Heatmap การใช้งาน":
    st.title("🔥 Heatmap ความเข้มข้นการใช้วัสดุ")
    st.info("แสดงปริมาณการเบิกของแต่ละช่าง × แต่ละวัสดุ "
            "— สีเข้ม = เบิกมาก, สีอ่อน = เบิกน้อย")

    # Period filter
    periods = ds.get_available_periods()
    period_filter = st.selectbox(
        "🗓️ เลือกช่วงเวลา",
        ["ทั้งหมด (สะสม)"] + periods)

    req = ds.get_requisitions()
    if req.empty:
        st.warning("ยังไม่มีข้อมูล")
    else:
        if period_filter != "ทั้งหมด (สะสม)":
            req["period"] = req.apply(
                lambda r: f"{int(r['month']):02d}/{int(r['year'])}"
                if pd.notna(r.get("month")) and pd.notna(r.get("year"))
                else None, axis=1)
            req = req[req["period"] == period_filter]

        if req.empty:
            st.info("ไม่มีข้อมูลในช่วงเวลาที่เลือก")
        else:
            pivot = req.pivot_table(
                index="employee_name", columns="material_name",
                values="quantity", aggfunc="sum", fill_value=0)

            fig = px.imshow(
                pivot.values,
                x=pivot.columns.tolist(),
                y=pivot.index.tolist(),
                color_continuous_scale="YlOrRd",
                aspect="auto",
                labels=dict(x="วัสดุ", y="ช่าง", color="จำนวน"),
            )
            fig.update_layout(
                height=max(400, len(pivot) * 28),
                xaxis=dict(tickangle=45),
                margin=dict(l=0, r=0, t=30, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Raw data expander
            with st.expander("📋 ดูตาราง Pivot"):
                st.dataframe(pivot, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# ⚠️ ตรวจจับความผิดปกติ — overall + per-material
# ═══════════════════════════════════════════════════════════════════
elif page == "⚠️ ตรวจจับความผิดปกติ":
    st.title("⚠️ ตรวจจับการเบิกผิดปกติ")

    threshold = st.slider("ค่า Z-Score Threshold", 1.0, 4.0, 2.0, 0.5)

    tab1, tab2 = st.tabs(["📊 ภาพรวม (ยอดรวมทุกวัสดุ)",
                           "🔬 รายวัสดุ (ผิดปกติเฉพาะรายการ)"])

    with tab1:
        anomalies = ds.get_anomalies(threshold)
        if anomalies.empty:
            st.success("✅ ไม่พบความผิดปกติ")
        else:
            st.warning(f"🚨 พบ {len(anomalies)} รายการที่น่าสงสัย")
            display_a = anomalies.copy()
            display_a.columns = ["ชื่อช่าง", "จำนวนเบิกรวม", "Z-Score"]
            display_a["Z-Score"] = display_a["Z-Score"].round(2)
            st.dataframe(display_a, use_container_width=True, hide_index=True)

        # All employees bar chart
        req = st.session_state["requisitions"]
        if not req.empty:
            all_usage = (req.groupby("employee_name")["quantity"]
                            .sum().sort_values(ascending=False).reset_index())
            mean_val = all_usage["quantity"].mean()
            fig = px.bar(all_usage, x="employee_name", y="quantity",
                         labels={"employee_name": "ช่าง",
                                 "quantity": "จำนวนเบิกรวม"})
            fig.add_hline(y=mean_val, line_dash="dash", line_color="red",
                          annotation_text=f"ค่าเฉลี่ย ({mean_val:.0f})")
            std_val = all_usage["quantity"].std()
            if std_val > 0:
                fig.add_hline(y=mean_val + threshold * std_val,
                              line_dash="dot", line_color="orange",
                              annotation_text=f"เกณฑ์ผิดปกติ (Z={threshold})")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("ตรวจจับช่างที่เบิก **วัสดุแต่ละชนิด** มากผิดปกติ "
                    "เมื่อเทียบกับช่างคนอื่นที่ใช้วัสดุชนิดเดียวกัน")
        per_mat = ds.get_anomalies_per_material(threshold)
        if per_mat.empty:
            st.success("✅ ไม่พบความผิดปกติเฉพาะรายการ")
        else:
            st.warning(f"🚨 พบ {len(per_mat)} คู่ ช่าง×วัสดุ ที่น่าสงสัย")
            display_pm = per_mat.copy()
            display_pm.columns = ["ชื่อช่าง", "วัสดุ", "จำนวน", "Z-Score"]
            display_pm["Z-Score"] = display_pm["Z-Score"].round(2)
            st.dataframe(display_pm, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# 🔍 ประวัติการใช้งาน (Audit Log)
# ═══════════════════════════════════════════════════════════════════
elif page == "🔍 ประวัติการใช้งาน":
    st.title("🔍 ประวัติการใช้งานระบบ")

    audit = ds.get_audit_log()
    if audit.empty:
        st.info("ยังไม่มีประวัติการใช้งาน")
    else:
        # Filter by action type
        actions = ["ทั้งหมด"] + sorted(audit["action"].dropna().unique().tolist())
        action_filter = st.selectbox("กรองตามประเภท", actions)

        display_audit = audit.sort_values("timestamp", ascending=False)
        if action_filter != "ทั้งหมด":
            display_audit = display_audit[display_audit["action"] == action_filter]
        display_audit = display_audit.head(200)

        display_audit = display_audit.rename(columns={
            "timestamp": "เวลา", "user": "ผู้ใช้",
            "action": "การกระทำ", "detail": "รายละเอียด"})
        st.dataframe(display_audit, use_container_width=True,
                     hide_index=True, height=500)

    # Purchase history
    pur = st.session_state["purchases"]
    if not pur.empty:
        with st.expander("📋 ประวัติการสั่งซื้อ (จาก Excel)"):
            cols = [c for c in ["item_name", "supplier_name", "quantity",
                                 "total_amount", "purchase_date",
                                 "sheet_category"] if c in pur.columns]
            display_pur = pur[cols].rename(columns={
                "item_name": "รายการ", "supplier_name": "ร้านค้า",
                "quantity": "จำนวน", "total_amount": "ยอดรวม",
                "purchase_date": "วันที่", "sheet_category": "หมวด"})
            st.dataframe(display_pur, use_container_width=True,
                         hide_index=True, height=400)