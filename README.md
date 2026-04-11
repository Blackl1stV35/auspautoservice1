# 🔧 SP Auto Service — ระบบจัดการวัสดุสิ้นเปลือง

ระบบ Streamlit สำหรับ **อู่เอสพี ออโต้เซอร์วิส** จ.ฉะเชิงเทรา  
แทนที่การจัดการ Excel ด้วยมือ ด้วยระบบเบิก-จ่ายวัสดุแบบดิจิทัล

## ⚡ Quick Start

```bash
# 1. Clone & เข้าโฟลเดอร์
git clone <your-repo-url>
cd sp-autoservice

# 2. สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. ติดตั้ง dependencies
pip install -r requirements.txt

# 4. รันแอป
streamlit run app.py
```

เปิดเบราว์เซอร์ไปที่ `http://localhost:8501`

## 📁 โครงสร้างโปรเจค

```
sp-autoservice/
├── app.py                  # Streamlit main app
├── src/
│   ├── etl.py              # ETL pipeline (Excel → CSV)
│   └── data_store.py       # CSV CRUD + Git commit
├── data/                   # CSV data (auto-generated, git-tracked)
├── .streamlit/config.toml  # Streamlit config
├── requirements.txt
└── README.md
```

## 🔄 วิธีใช้งาน

1. **อัปโหลด Excel** — ใช้เมนู "อัปโหลด Excel" นำไฟล์ Excel เดิม 2 ไฟล์เข้าระบบ
2. **เบิกวัสดุ** — เลือกชื่อช่าง → เลือกวัสดุ → ใส่จำนวน → ยืนยัน
3. **ดูสต็อก** — ตรวจสอบสต็อกปัจจุบัน รับวัสดุเข้าสต็อกได้
4. **รายงาน** — ดูสถิติการเบิกรายช่าง ตรวจจับความผิดปกติ

## 📝 หมายเหตุ

- ข้อมูลทั้งหมดเก็บเป็น CSV ใน `data/`
- ทุกการเปลี่ยนแปลงจะ commit อัตโนมัติไปยัง Git
- รองรับภาษาไทยทั้งระบบ
- ใช้ได้บนมือถือ/แท็บเล็ต

## 🗺️ Phase 2 (อนาคต)

- Barcode/QR Scanner
- LINE Bot แจ้งเตือน
- Supabase cloud database
