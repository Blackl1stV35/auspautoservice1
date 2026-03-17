import os
import requests
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from src.config import logger, LINE_CHANNEL_ACCESS_TOKEN, supabase
from src.nlp_engine import transcribe_audio, parse_requisition_text
from src.db_operations import get_or_create_employee, get_or_create_material
from src.ai_engine import run_ai_analysis
from src.etl_pipeline import run_etl_pipeline

app = FastAPI(title="Auto Shop AI API")

LINE_HEADERS = {
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def reply_to_line(reply_token: str, text: str):
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=LINE_HEADERS, json=payload)

def process_line_message(message_id: str, message_type: str, text: str, reply_token: str):
    transcript = text
    
    if message_type == "audio":
        audio_url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
        res = requests.get(audio_url, headers={"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"})
        
        audio_path = f"temp_{message_id}.m4a"
        with open(audio_path, 'wb') as f:
            f.write(res.content)
        
        transcript = transcribe_audio(audio_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
    if not transcript:
        reply_to_line(reply_token, "❌ ไม่สามารถฟังเสียงได้ชัดเจน รบกวนพิมพ์ข้อความครับ")
        return
        
    parsed_data = parse_requisition_text(transcript)
    if not parsed_data or "employee_name" not in parsed_data:
        reply_to_line(reply_token, "❌ AI ไม่สามารถแยกข้อมูลได้ รบกวนพิมพ์ใหม่อีกครั้งครับ")
        return
        
    try:
        emp_name = parsed_data.get("employee_name", "Unknown")
        item_name = parsed_data.get("item_name", "Unknown")
        qty = float(parsed_data.get("quantity", 1.0)) # Default to 1

        emp_id = get_or_create_employee(emp_name)
        mat_id = get_or_create_material(item_name)
        
        supabase.table("transactions").insert({
            "employee_id": emp_id,
            "material_id": mat_id,
            "quantity": qty
        }).execute()
        
        reply_to_line(reply_token, f"✅ บันทึกสำเร็จ:\nพนักงาน: {emp_name}\nเบิก: {item_name}\nจำนวน: {qty}")
        logger.info(f"LINE TX saved: {emp_name} took {qty} of {item_name}")
        
    except Exception as e:
        logger.error(f"DB Insert Error: {e}")
        reply_to_line(reply_token, "❌ เกิดข้อผิดพลาดในการบันทึกลงฐานข้อมูล")

# Added both routes to catch traffic regardless of LINE configuration
@app.post("/webhook")
@app.post("/callback")
async def line_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    for event in body.get("events", []):
        if event.get("type") == "message":
            reply_token = event["replyToken"]
            msg = event["message"]
            msg_type = msg["type"]
            msg_id = msg["id"]
            text = msg.get("text", "")
            
            if msg_type in ["text", "audio"]:
                background_tasks.add_task(process_line_message, msg_id, msg_type, text, reply_token)
                
    return {"status": "ok"}

@app.post("/trigger-etl")
def api_trigger_etl():
    req_file = r"data\เอสพี--สถิติเบิกวัสดุสิ้นเปลือง(69).xlsx"
    pur_file = r"data\3--เอสพี--ต้นทุนแผนกสี และน้ำมัน และกิ๊บน๊อต.xlsx"
    try:
        run_etl_pipeline(req_file, pur_file)
        run_ai_analysis()
        return {"status": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))