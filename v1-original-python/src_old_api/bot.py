import os
import requests
from fastapi import FastAPI, Request, BackgroundTasks
from src.core.config import logger, LINE_CHANNEL_ACCESS_TOKEN, supabase
from src.nlp.nlp_engine import transcribe_audio, parse_requisition_text
from src.core.db import get_or_create_employee, get_or_create_material

app = FastAPI(title="Auto Shop API")

LINE_HEADERS = {"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}", "Content-Type": "application/json"}

def reply_to_line(reply_token: str, text: str):
    requests.post("https://api.line.me/v2/bot/message/reply", headers=LINE_HEADERS, json={
        "replyToken": reply_token, "messages": [{"type": "text", "text": text}]
    })

def process_line_message(message_id: str, message_type: str, text: str, reply_token: str):
    transcript = text
    if message_type == "audio":
        audio_url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
        res = requests.get(audio_url, headers={"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"})
        audio_path = f"temp_{message_id}.m4a"
        with open(audio_path, 'wb') as f: f.write(res.content)
        transcript = transcribe_audio(audio_path)
        if os.path.exists(audio_path): os.remove(audio_path)
            
    if not transcript:
        reply_to_line(reply_token, "❌ ไม่สามารถฟังเสียงได้ชัดเจน รบกวนพิมพ์ข้อความครับ")
        return
        
    parsed = parse_requisition_text(transcript)
    if not parsed or "employee_name" not in parsed:
        reply_to_line(reply_token, "❌ AI ไม่สามารถแยกข้อมูลได้ รบกวนพิมพ์ใหม่อีกครั้งครับ")
        return
        
    try:
        emp_name, item_name, qty = parsed.get("employee_name", "Unknown"), parsed.get("item_name", "Unknown"), float(parsed.get("quantity", 1.0))
        supabase.table("transactions").insert({
            "employee_id": get_or_create_employee(emp_name),
            "material_id": get_or_create_material(item_name),
            "quantity": qty
        }).execute()
        reply_to_line(reply_token, f"✅ บันทึกสำเร็จ:\nพนักงาน: {emp_name}\nเบิก: {item_name}\nจำนวน: {qty}")
    except Exception as e:
        logger.error(f"DB Insert Error: {e}")
        reply_to_line(reply_token, "❌ เกิดข้อผิดพลาดในการบันทึกลงฐานข้อมูล")

@app.post("/webhook")
@app.post("/callback")
async def line_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    for event in body.get("events", []):
        if event.get("type") == "message":
            msg = event["message"]
            if msg["type"] in ["text", "audio"]:
                background_tasks.add_task(process_line_message, msg["id"], msg["type"], msg.get("text", ""), event["replyToken"])
    return {"status": "ok"}