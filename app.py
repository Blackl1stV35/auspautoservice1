"""
SP Auto Service v4 — ระบบจัดการวัสดุสิ้นเปลือง (Supabase + Cost Analysis)
อู่เอสพี ออโต้เซอร์วิส จ.ฉะเชิงเทรา
"""
import streamlit as st
import pandas as pd
import os, sys
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.etl import run_full_etl, generate_clean_excel
from src import data_store as ds

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

st.set_page_config(page_title="SP Auto Service", page_icon="🔧",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
    .stSelectbox label,.stNumberInput label,.stTextInput label{font-size:1.1rem!important;font-weight:600!important}
    div[data-testid="stMetric"]{background:#f8f9fa;border-radius:10px;padding:12px;border-left:4px solid #FF6B35}
    .success-box{background:#d4edda;padding:1rem;border-radius:8px;margin:.5rem 0;border-left:4px solid #28a745;font-size:1.1rem}
    .dup-box{background:#fff3cd;padding:1rem;border-radius:8px;margin:.5rem 0;border-left:4px solid #ffc107;font-size:1.1rem}
    .tx-id{color:#6c757d;font-size:.85rem}
</style>""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/car-service.png", width=64)
st.sidebar.title("🔧 SP Auto Service")
st.sidebar.caption("v4.0 — Supabase + Cost Analysis")

page = st.sidebar.radio("เมนู", [
    "🏠 หน้าหลัก", "📤 อัปโหลด Excel", "📝 เบิกวัสดุ", "📦 สต็อกวัสดุ",
    "📊 รายงานช่าง", "🗓️ สรุปรายเดือน", "🔥 Heatmap การใช้งาน",
    "💰 Cost & Supplier", "⚠️ ตรวจจับความผิดปกติ", "🔍 ประวัติการใช้งาน",
])

st.sidebar.divider()
_db = ds.db_status_info()
st.sidebar.caption(f"{'🟢' if _db['connected'] else '🔴'} Supabase: {_db.get('project','ไม่เชื่อมต่อ')}")
st.sidebar.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")


# ═══════════════════════════════════════════════════════════════════
# 🏠 หน้าหลัก
# ═══════════════════════════════════════════════════════════════════
if page == "🏠 หน้าหลัก":
    st.title("🏠 ภาพรวมระบบ")
    req, emp, mat, stock = ds.get_requisitions(), ds.get_employees(), ds.get_materials(), ds.get_stock()
    low = ds.get_low_stock()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👷 ช่าง", len(emp) if not emp.empty else 0)
    c2.metric("🧰 วัสดุ", len(mat) if not mat.empty else 0)
    c3.metric("📋 เบิก", len(req) if not req.empty else 0)
    c4.metric("⚠️ ใกล้หมด", len(low) if not low.empty else 0)

    if not req.empty and "material_name" in req.columns:
        st.divider()
        left, right = st.columns(2)
        with left:
            st.subheader("🏆 Top 10 วัสดุ")
            top = req.groupby("material_name")["quantity"].sum().nlargest(10).reset_index()
            fig = px.bar(top, x="quantity", y="material_name", orientation="h",
                         color="quantity", color_continuous_scale="Oranges",
                         labels={"quantity": "จำนวน", "material_name": "วัสดุ"})
            fig.update_layout(yaxis=dict(autorange="reversed"), height=380, showlegend=False,
                              margin=dict(l=0, r=10, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)
        with right:
            st.subheader("👷 Top 10 ช่าง")
            top = req.groupby("employee_name")["quantity"].sum().nlargest(10).reset_index()
            fig = px.bar(top, x="quantity", y="employee_name", orientation="h",
                         color="quantity", color_continuous_scale="Blues",
                         labels={"quantity": "จำนวน", "employee_name": "ช่าง"})
            fig.update_layout(yaxis=dict(autorange="reversed"), height=380, showlegend=False,
                              margin=dict(l=0, r=10, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)

    if not low.empty:
        st.subheader("⚠️ วัสดุใกล้หมด")
        ld = low[["item_name", "current_qty"]].copy()
        ld["สถานะ"] = ld["current_qty"].apply(ds.get_stock_status)
        ld.rename(columns={"item_name": "วัสดุ", "current_qty": "คงเหลือ"}, inplace=True)
        st.dataframe(ld, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# 📤 อัปโหลด Excel
# ═══════════════════════════════════════════════════════════════════
elif page == "📤 อัปโหลด Excel":
    st.title("📤 อัปโหลดไฟล์ Excel")
    col1, col2 = st.columns(2)
    with col1:
        req_file = st.file_uploader("📄 ไฟล์เบิกวัสดุ", type=["xlsx", "xls"], key="req_up")
    with col2:
        pur_file = st.file_uploader("📄 ไฟล์ต้นทุน/สั่งซื้อ", type=["xlsx", "xls"], key="pur_up")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 ประมวลผล → Supabase", type="primary", use_container_width=True):
            if not req_file and not pur_file:
                st.error("กรุณาอัปโหลดไฟล์อย่างน้อย 1 ไฟล์")
            else:
                os.makedirs(DATA_DIR, exist_ok=True)
                rp = pp = None
                if req_file:
                    rp = os.path.join(DATA_DIR, "upload_req.xlsx")
                    with open(rp, "wb") as f: f.write(req_file.read())
                if pur_file:
                    pp = os.path.join(DATA_DIR, "upload_pur.xlsx")
                    with open(pp, "wb") as f: f.write(pur_file.read())
                with st.spinner("⏳ กำลังประมวลผล..."):
                    try:
                        result = run_full_etl(rp, pp)
                        st.markdown('<div class="success-box">✅ บันทึกลง Supabase สำเร็จ!</div>',
                                    unsafe_allow_html=True)
                        for k, lbl in [("requisitions","เบิก"),("employees","ช่าง"),
                                       ("materials","วัสดุ"),("purchases","ซื้อ")]:
                            if k in result and not result[k].empty:
                                st.success(f"📊 {lbl}: {len(result[k])} รายการ")
                    except Exception as e:
                        st.error(f"❌ {e}")

    with c2:
        if st.button("📥 Backup Clean Excel", use_container_width=True):
            rp = os.path.join(DATA_DIR, "upload_req.xlsx") if req_file or os.path.exists(os.path.join(DATA_DIR, "upload_req.xlsx")) else None
            pp = os.path.join(DATA_DIR, "upload_pur.xlsx") if pur_file or os.path.exists(os.path.join(DATA_DIR, "upload_pur.xlsx")) else None
            if not rp and not pp:
                st.warning("กรุณาอัปโหลดไฟล์ก่อน")
            else:
                rp = rp if rp and os.path.exists(rp) else None
                pp = pp if pp and os.path.exists(pp) else None
                with st.spinner("กำลังสร้างไฟล์ Clean Excel..."):
                    data = generate_clean_excel(rp, pp)
                    st.download_button("⬇️ ดาวน์โหลด Clean Excel", data,
                                       f"SP_Clean_{datetime.now():%Y%m%d}.xlsx",
                                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ═══════════════════════════════════════════════════════════════════
# 📝 เบิกวัสดุ
# ═══════════════════════════════════════════════════════════════════
elif page == "📝 เบิกวัสดุ":
    st.title("📝 ฟอร์มเบิกวัสดุ")
    emp, mat = ds.get_employees(), ds.get_materials()
    if emp.empty or mat.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลช่าง/วัสดุ กรุณาอัปโหลด Excel ก่อน")
    else:
        emp_names = sorted(emp["name"].dropna().unique().tolist())
        mat_names = sorted(mat["item_name"].dropna().unique().tolist())
        c1, c2 = st.columns(2)
        with c1: sel_emp = st.selectbox("👷 ชื่อช่าง", emp_names)
        with c2: sel_mat = st.selectbox("🧰 วัสดุ", mat_names)
        quantity = st.number_input("📦 จำนวน", min_value=1, max_value=100, value=1)
        issued_by = st.text_input("🔑 ผู้บันทึก", value="admin")

        stock = ds.get_stock()
        if not stock.empty and "item_name" in stock.columns:
            ms = stock[stock["item_name"] == sel_mat]
            if not ms.empty:
                c = int(ms.iloc[0].get("current_qty", 0))
                st.info(f"📦 สต็อก: **{sel_mat}** = **{c}** ชิ้น {ds.get_stock_status(c)}")

        st.divider()
        st.markdown(f"**สรุป:** {sel_emp} เบิก **{sel_mat}** จำนวน **{quantity}** ชิ้น")
        if st.button("✅ ยืนยันเบิก", type="primary", use_container_width=True):
            r = ds.issue_material(sel_emp, sel_mat, quantity, issued_by)
            if r["ok"]:
                st.markdown(f'<div class="success-box">{r["msg"]}</div>'
                            f'<div class="tx-id">🔖 {r["tx_id"]} 💾</div>',
                            unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f'<div class="dup-box">{r["msg"]}</div>', unsafe_allow_html=True)

        req = ds.get_requisitions()
        if not req.empty:
            with st.expander("📋 ล่าสุด 20 รายการ"):
                cols = [c for c in ["tx_id","date","time","employee_name","material_name","quantity","issued_by"] if c in req.columns]
                st.dataframe(req[cols].head(20).rename(columns={
                    "tx_id":"รหัส","date":"วันที่","time":"เวลา","employee_name":"ช่าง",
                    "material_name":"วัสดุ","quantity":"จำนวน","issued_by":"ผู้บันทึก"}),
                    use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# 📦 สต็อกวัสดุ
# ═══════════════════════════════════════════════════════════════════
elif page == "📦 สต็อกวัสดุ":
    st.title("📦 สต็อกวัสดุปัจจุบัน")
    stock = ds.get_stock()
    if stock.empty:
        st.warning("⚠️ ยังไม่มีข้อมูลสต็อก")
    else:
        search = st.text_input("🔍 ค้นหา", "")
        disp = stock.copy()
        if search:
            disp = disp[disp["item_name"].str.contains(search, case=False, na=False)]
        disp["status"] = disp["current_qty"].apply(ds.get_stock_status)
        cols = [c for c in ["item_name","current_qty","status","last_updated"] if c in disp.columns]
        rn = {"item_name":"วัสดุ","current_qty":"คงเหลือ","status":"สถานะ","last_updated":"อัปเดต"}
        styled = disp[cols].rename(columns=rn)

        def hl(row):
            q = 99
            try: q = int(row.get("คงเหลือ",99))
            except: pass
            if q <= 0: return ["background-color:#f5c6cb"]*len(row)
            if q <= 5: return ["background-color:#f8d7da"]*len(row)
            if q <= 10: return ["background-color:#fff3cd"]*len(row)
            return [""]*len(row)

        st.dataframe(styled.style.apply(hl, axis=1), use_container_width=True, hide_index=True, height=500)

        if len(disp) > 0:
            sc = disp["status"].value_counts().reset_index()
            sc.columns = ["สถานะ","จำนวน"]
            fig = px.pie(sc, values="จำนวน", names="สถานะ", color="สถานะ",
                         color_discrete_map={"🔴 หมด":"#dc3545","🟠 วิกฤต":"#fd7e14",
                                             "🟡 ต่ำ":"#ffc107","🟢 ปกติ":"#28a745"})
            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("➕ รับวัสดุเข้า")
        c1,c2,c3 = st.columns(3)
        mn = sorted(stock["item_name"].dropna().unique().tolist())
        with c1: am = st.selectbox("วัสดุ", mn, key="as_m")
        with c2: aq = st.number_input("จำนวน", min_value=1, value=10, key="as_q")
        with c3: au = st.text_input("ผู้รับ", value="admin", key="as_u")
        if st.button("✅ รับเข้า", type="primary"):
            r = ds.add_stock(am, aq, au)
            st.success(r["msg"]) if r.get("ok") else st.warning(r.get("msg","error"))
            st.rerun()


# ═══════════════════════════════════════════════════════════════════
# 📊 รายงานช่าง
# ═══════════════════════════════════════════════════════════════════
elif page == "📊 รายงานช่าง":
    st.title("📊 รายงานช่าง")
    req = ds.get_requisitions()
    if req.empty:
        st.warning("⚠️ ไม่มีข้อมูล")
    else:
        mode = st.radio("มุมมอง", ["ภาพรวม","รายเดือน","รายบุคคล"], horizontal=True)
        if mode == "ภาพรวม":
            u = req.groupby("employee_name")["quantity"].sum().sort_values(ascending=False).reset_index()
            u.columns = ["ชื่อช่าง","จำนวน"]
            st.dataframe(u, use_container_width=True, hide_index=True)
            fig = px.bar(u.head(15), x="ชื่อช่าง", y="จำนวน", color="จำนวน", color_continuous_scale="Reds")
            st.plotly_chart(fig, use_container_width=True)
        elif mode == "รายเดือน":
            pv = ds.get_monthly_summary()
            if pv.empty: st.info("ไม่มีข้อมูล")
            else: st.dataframe(pv, use_container_width=True)
        else:
            names = sorted(req["employee_name"].dropna().unique().tolist())
            sel = st.selectbox("เลือกช่าง", names)
            er = req[req["employee_name"]==sel]
            bm = er.groupby("material_name")["quantity"].sum().sort_values(ascending=False).reset_index()
            bm.columns = ["วัสดุ","จำนวน"]
            st.metric("เบิกทั้งหมด", int(bm["จำนวน"].sum()))
            st.dataframe(bm, use_container_width=True, hide_index=True)
            fig = px.pie(bm.head(10), values="จำนวน", names="วัสดุ")
            st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# 🗓️ สรุปรายเดือน
# ═══════════════════════════════════════════════════════════════════
elif page == "🗓️ สรุปรายเดือน":
    st.title("🗓️ สรุปรายเดือน")
    t1, t2 = st.tabs(["👷 ช่าง×เดือน", "🧰 วัสดุ×เดือน"])
    with t1:
        pv = ds.get_monthly_summary()
        if pv.empty: st.warning("ไม่มีข้อมูล")
        else:
            st.dataframe(pv, use_container_width=True, height=500)
            tot = pv["รวมทั้งหมด"].reset_index(); tot.columns = ["ช่าง","รวม"]
            fig = px.bar(tot.sort_values("รวม",ascending=False).head(15), x="ช่าง", y="รวม",
                         color="รวม", color_continuous_scale="Reds")
            st.plotly_chart(fig, use_container_width=True)
    with t2:
        pv = ds.get_monthly_by_material()
        if pv.empty: st.warning("ไม่มีข้อมูล")
        else:
            st.dataframe(pv, use_container_width=True, height=500)
            tot = pv["รวมทั้งหมด"].reset_index(); tot.columns = ["วัสดุ","รวม"]
            fig = px.bar(tot.sort_values("รวม",ascending=False).head(15), x="วัสดุ", y="รวม",
                         color="รวม", color_continuous_scale="Oranges")
            st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# 🔥 Heatmap
# ═══════════════════════════════════════════════════════════════════
elif page == "🔥 Heatmap การใช้งาน":
    st.title("🔥 Heatmap การใช้วัสดุ")
    periods = ds.get_available_periods()
    pf = st.selectbox("🗓️ ช่วงเวลา", ["ทั้งหมด"] + periods)
    req = ds.get_requisitions()
    if req.empty:
        st.warning("ไม่มีข้อมูล")
    else:
        if pf != "ทั้งหมด":
            req = req.copy()
            req["period"] = req.apply(
                lambda r: f"{int(r['month']):02d}/{int(r['year'])}"
                if pd.notna(r.get("month")) and pd.notna(r.get("year")) else None, axis=1)
            req = req[req["period"]==pf]
        if req.empty:
            st.info("ไม่มีข้อมูลช่วงนี้")
        else:
            pv = req.pivot_table(index="employee_name", columns="material_name",
                                  values="quantity", aggfunc="sum", fill_value=0)
            fig = px.imshow(pv.values, x=pv.columns.tolist(), y=pv.index.tolist(),
                            color_continuous_scale="YlOrRd", aspect="auto",
                            labels=dict(x="วัสดุ",y="ช่าง",color="จำนวน"))
            fig.update_layout(height=max(400,len(pv)*28), xaxis=dict(tickangle=45))
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("📋 ตาราง"): st.dataframe(pv, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# 💰 Cost & Supplier Analysis ★ NEW
# ═══════════════════════════════════════════════════════════════════
elif page == "💰 Cost & Supplier":
    st.title("💰 Cost & Supplier Analysis")

    # ── KPI Cards ──
    kpi = ds.get_cost_kpis()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💵 ยอดรวมทั้งหมด", f"฿{kpi['total_spend']:,.0f}")
    c2.metric("📅 เดือนนี้", f"฿{kpi['this_month']:,.0f}")
    c3.metric("📊 YTD", f"฿{kpi['ytd_spend']:,.0f}")
    c4.metric("📈 เฉลี่ย/วัน", f"฿{kpi['avg_daily']:,.0f}")

    if kpi["top_drivers"]:
        st.caption("🔝 Top cost drivers: " + " | ".join(
            f"**{d[0]}** ฿{d[1]:,.0f}" for d in kpi["top_drivers"]))

    st.divider()
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 แนวโน้มรายเดือน", "📦 หมวดหมู่", "🏪 ซัพพลายเออร์",
        "⚡ ราคาผิดปกติ", "📊 ซื้อ vs เบิก"
    ])

    # ── Tab 1: Monthly Cost Trend ──
    with tab1:
        mc = ds.get_monthly_cost()
        if mc.empty:
            st.info("ไม่มีข้อมูลต้นทุน")
        else:
            monthly_total = mc.groupby("period")["total_cost"].sum().reset_index().sort_values("period")
            fig = px.line(monthly_total, x="period", y="total_cost", markers=True,
                          labels={"period":"เดือน","total_cost":"ต้นทุนรวม (บาท)"},
                          title="แนวโน้มต้นทุนรายเดือน")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Stacked by category
            by_cat = mc.groupby(["period","sheet_category"])["total_cost"].sum().reset_index()
            fig2 = px.bar(by_cat, x="period", y="total_cost", color="sheet_category",
                          labels={"period":"เดือน","total_cost":"บาท","sheet_category":"หมวด"},
                          title="ต้นทุนรายเดือน แยกตามหมวด")
            st.plotly_chart(fig2, use_container_width=True)

            # Forecast
            fc = ds.get_cost_forecast()
            if not fc.empty and "forecast" in fc.columns:
                st.subheader("🔮 พยากรณ์ต้นทุน (3-month MA)")
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(x=fc["period"], y=fc["total_cost"],
                                          mode="lines+markers", name="ต้นทุนจริง"))
                fig3.add_trace(go.Scatter(x=fc["period"], y=fc["forecast"],
                                          mode="lines", name="พยากรณ์", line=dict(dash="dash")))
                overbudget = fc[fc["over_budget"]==True]
                if not overbudget.empty:
                    fig3.add_trace(go.Scatter(x=overbudget["period"], y=overbudget["total_cost"],
                                              mode="markers", name="⚠️ เกินงบ",
                                              marker=dict(size=14, color="red", symbol="x")))
                fig3.update_layout(height=350)
                st.plotly_chart(fig3, use_container_width=True)

    # ── Tab 2: Category Breakdown ──
    with tab2:
        cat = ds.get_category_cost()
        if cat.empty:
            st.info("ไม่มีข้อมูล")
        else:
            c1, c2 = st.columns(2)
            with c1:
                fig = px.pie(cat, values="total_cost", names="category",
                             title="สัดส่วนต้นทุนตามหมวด", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig = px.bar(cat.sort_values("total_cost", ascending=False),
                             x="category", y="total_cost", color="total_cost",
                             color_continuous_scale="Reds",
                             labels={"category":"หมวด","total_cost":"บาท"})
                st.plotly_chart(fig, use_container_width=True)
            st.dataframe(cat.rename(columns={"category":"หมวด","item_count":"จำนวนรายการ",
                                              "total_cost":"ต้นทุนรวม","avg_cost":"เฉลี่ย/รายการ"}),
                         use_container_width=True, hide_index=True)

    # ── Tab 3: Supplier Ranking ──
    with tab3:
        sup = ds.get_supplier_ranking()
        if sup.empty:
            st.info("ไม่มีข้อมูล")
        else:
            st.subheader("🏪 อันดับซัพพลายเออร์")
            fig = px.bar(sup.head(15), x="supplier_name", y="total_spend",
                         color="total_spend", color_continuous_scale="Blues",
                         labels={"supplier_name":"ร้านค้า","total_spend":"ยอดรวม (บาท)"})
            st.plotly_chart(fig, use_container_width=True)
            rn = {"supplier_name":"ร้านค้า","order_count":"จำนวนครั้ง","total_spend":"ยอดรวม",
                  "total_qty":"จำนวนชิ้น","unique_items":"รายการ"}
            cols = [c for c in rn.keys() if c in sup.columns]
            st.dataframe(sup[cols].rename(columns=rn), use_container_width=True, hide_index=True)

    # ── Tab 4: Price Spikes ──
    with tab4:
        threshold = st.slider("เกณฑ์ราคาเพิ่ม (%)", 10, 100, 30, 5)
        spikes = ds.get_price_spikes(threshold)
        if spikes.empty:
            st.success(f"✅ ไม่พบราคาเพิ่มขึ้น > {threshold}%")
        else:
            st.warning(f"🚨 พบ {len(spikes)} รายการที่ราคาเพิ่ม > {threshold}%")
            spikes_display = spikes.copy()
            spikes_display["pct_change"] = spikes_display["pct_change"].round(1)
            spikes_display.rename(columns={
                "item_name":"รายการ","supplier_name":"ร้านค้า","purchase_date":"วันที่",
                "prev_price":"ราคาเดิม","price_per_unit":"ราคาใหม่","pct_change":"เพิ่ม %"
            }, inplace=True)
            st.dataframe(spikes_display, use_container_width=True, hide_index=True)

    # ── Tab 5: Cost vs Usage ──
    with tab5:
        cvu = ds.get_cost_vs_usage()
        if cvu.empty:
            st.info("ไม่มีข้อมูล")
        else:
            st.subheader("📊 ซื้อเข้า vs เบิกออก")
            fig = go.Figure()
            cvu_sorted = cvu.sort_values("purchase_cost", ascending=False).head(20)
            fig.add_trace(go.Bar(x=cvu_sorted["item_name"], y=cvu_sorted["purchased_qty"],
                                 name="ซื้อเข้า", marker_color="#4e79a7"))
            fig.add_trace(go.Bar(x=cvu_sorted["item_name"], y=cvu_sorted["issued_qty"],
                                 name="เบิกออก", marker_color="#e15759"))
            fig.update_layout(barmode="group", height=400,
                              xaxis=dict(tickangle=45),
                              legend=dict(orientation="h", yanchor="bottom", y=1.02))
            st.plotly_chart(fig, use_container_width=True)

            # Overstock / understock table
            st.subheader("📦 สถานะ สต็อกเกิน / สต็อกต่ำ")
            alert = cvu[cvu["stock_status"] != "ปกติ"].sort_values("stock_status")
            if alert.empty:
                st.success("✅ สต็อกทุกรายการปกติ")
            else:
                alert_display = alert[["item_name","purchased_qty","issued_qty","current_stock","stock_status"]].copy()
                alert_display.rename(columns={
                    "item_name":"รายการ","purchased_qty":"ซื้อเข้า","issued_qty":"เบิกออก",
                    "current_stock":"คงเหลือ","stock_status":"สถานะ"
                }, inplace=True)
                st.dataframe(alert_display, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# ⚠️ ตรวจจับความผิดปกติ
# ═══════════════════════════════════════════════════════════════════
elif page == "⚠️ ตรวจจับความผิดปกติ":
    st.title("⚠️ ตรวจจับความผิดปกติ")
    threshold = st.slider("Z-Score", 1.0, 4.0, 2.0, 0.5)
    t1, t2 = st.tabs(["📊 ภาพรวม", "🔬 รายวัสดุ"])
    with t1:
        anom = ds.get_anomalies(threshold)
        if anom.empty:
            st.success("✅ ไม่พบ")
        else:
            st.warning(f"🚨 พบ {len(anom)} รายการ")
            da = anom.copy(); da.columns = ["ช่าง","จำนวน","Z-Score"]
            da["Z-Score"] = da["Z-Score"].round(2)
            st.dataframe(da, use_container_width=True, hide_index=True)
        req = ds.get_requisitions()
        if not req.empty:
            au = req.groupby("employee_name")["quantity"].sum().sort_values(ascending=False).reset_index()
            mv = au["quantity"].mean()
            fig = px.bar(au, x="employee_name", y="quantity",
                         labels={"employee_name":"ช่าง","quantity":"เบิกรวม"})
            fig.add_hline(y=mv, line_dash="dash", line_color="red",
                          annotation_text=f"เฉลี่ย ({mv:.0f})")
            sv = au["quantity"].std()
            if sv > 0:
                fig.add_hline(y=mv+threshold*sv, line_dash="dot", line_color="orange",
                              annotation_text=f"เกณฑ์ (Z={threshold})")
            st.plotly_chart(fig, use_container_width=True)
    with t2:
        pm = ds.get_anomalies_per_material(threshold)
        if pm.empty:
            st.success("✅ ไม่พบ")
        else:
            st.warning(f"🚨 พบ {len(pm)} คู่")
            dp = pm.copy(); dp.columns = ["ช่าง","วัสดุ","จำนวน","Z-Score"]
            dp["Z-Score"] = dp["Z-Score"].round(2)
            st.dataframe(dp, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════
# 🔍 ประวัติ
# ═══════════════════════════════════════════════════════════════════
elif page == "🔍 ประวัติการใช้งาน":
    st.title("🔍 ประวัติการใช้งาน")
    audit = ds.get_audit_log()
    if audit.empty:
        st.info("ยังไม่มีประวัติ")
    else:
        actions = ["ทั้งหมด"] + sorted(audit["action"].dropna().unique().tolist())
        af = st.selectbox("กรอง", actions)
        da = audit.copy()
        if af != "ทั้งหมด": da = da[da["action"]==af]
        da = da.head(200).rename(columns={"timestamp":"เวลา","user":"ผู้ใช้","action":"กระทำ","detail":"รายละเอียด"})
        st.dataframe(da, use_container_width=True, hide_index=True, height=500)

    pur = ds.get_purchases()
    if not pur.empty:
        with st.expander("📋 ประวัติสั่งซื้อ"):
            cols = [c for c in ["item_name","supplier_name","quantity","total_amount","purchase_date","sheet_category"] if c in pur.columns]
            st.dataframe(pur[cols].rename(columns={
                "item_name":"รายการ","supplier_name":"ร้านค้า","quantity":"จำนวน",
                "total_amount":"ยอดรวม","purchase_date":"วันที่","sheet_category":"หมวด"}),
                use_container_width=True, hide_index=True, height=400)
