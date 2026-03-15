import os
import json
import requests
from fastapi import FastAPI, Request, BackgroundTasks
from supabase import create_client, Client
from groq import Groq
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

app = FastAPI(title="SP Inventory PoC Pipeline")

# Initialize Supabase
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Initialize Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# LINE API Headers
LINE_HEADERS = {
    "Authorization": f"Bearer {os.getenv('LINE_CHANNEL_ACCESS_TOKEN')}",
    "Content-Type": "application/json"
}

def process_audio_to_text(message_id: str) -> str:
    """Downloads audio from LINE and sends to Groq Whisper for transcription."""
    # 1. Get audio content from LINE
    line_audio_url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    response = requests.get(line_audio_url, headers={"Authorization": f"Bearer {os.getenv('LINE_CHANNEL_ACCESS_TOKEN')}"})
    
    # Save temporarily
    audio_path = f"temp_{message_id}.m4a"
    with open(audio_path, 'wb') as f:
        f.write(response.content)

    # 2. Send to Groq Whisper
    with open(audio_path, "rb") as file:
        transcription = groq_client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3",
            prompt="Transcribe Thai language accurately, including factory terms like ทินเนอร์, สีโป๊ว, กิ๊บ.",
            response_format="text",
            language="th"
        )
    
    os.remove(audio_path) # Clean up
    return transcription

def parse_text_with_typhoon(transcript: str) -> dict:
    """Sends transcript to local Ollama (Typhoon) to extract structured JSON."""
    
    # The System Prompt is crucial for the AI to match your Supabase tables
    system_prompt = """
    You are a data extraction assistant for a Thai auto body shop. 
    Extract the employee name, material name, and quantity from the user's text.
    Return strictly a JSON object with keys: "employee_name", "item_name", "quantity".
    Do not include markdown formatting or any other text.
    """

    ollama_payload = {
        "model": "scb10x/llama3.2-typhoon2-3b-instruct",
        "prompt": f"{system_prompt}\n\nUser input: {transcript}",
        "stream": False,
        "format": "json" # Forces JSON output
    }

    # Call local Ollama API
    response = requests.post("http://localhost:11434/api/generate", json=ollama_payload)
    result = response.json()
    
    try:
        return json.loads(result["response"])
    except:
        return None # Handle parsing errors in production

def save_to_supabase(parsed_data: dict) -> str:
    """Maps names to IDs and saves transaction to Supabase."""
    try:
        # 1. Find Employee ID
        emp_res = supabase.table("employees").select("id").ilike("name", f"%{parsed_data['employee_name']}%").execute()
        if not emp_res.data: return "ไม่พบชื่อพนักงานในระบบ"
        emp_id = emp_res.data[0]['id']

        # 2. Find Material ID
        mat_res = supabase.table("materials").select("id").ilike("item_name", f"%{parsed_data['item_name']}%").execute()
        if not mat_res.data: return "ไม่พบรายการวัสดุในระบบ"
        mat_id = mat_res.data[0]['id']

        # 3. Insert Transaction
        supabase.table("transactions").insert({
            "employee_id": emp_id,
            "material_id": mat_id,
            "quantity": parsed_data["quantity"]
        }).execute()

        return f"✅ บันทึกสำเร็จ: {parsed_data['employee_name']} เบิก {parsed_data['item_name']} จำนวน {parsed_data['quantity']}"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"

def reply_to_line(reply_token: str, text: str):
    """Sends a reply message back to the LINE user."""
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=LINE_HEADERS, json=payload)

@app.post("/webhook")
async def line_webhook(request: Request, background_tasks: BackgroundTasks):
    """Main endpoint to receive LINE webhooks."""
    body = await request.json()
    
    for event in body.get("events", []):
        if event["type"] == "message":
            reply_token = event["replyToken"]
            message_type = event["message"]["type"]
            
            # Run the heavy processing in the background so LINE doesn't timeout
            if message_type == "audio":
                background_tasks.add_task(process_pipeline, event["message"]["id"], reply_token, is_audio=True)
            elif message_type == "text":
                text = event["message"]["text"]
                background_tasks.add_task(process_pipeline, text, reply_token, is_audio=False)

    return {"status": "ok"}

def process_pipeline(input_data: str, reply_token: str, is_audio: bool):
    """The orchestration function running in the background."""
    if is_audio:
        transcript = process_audio_to_text(input_data)
    else:
        transcript = input_data # Input was just text

    parsed_json = parse_text_with_typhoon(transcript)
    
    if parsed_json:
        result_message = save_to_supabase(parsed_json)
        reply_to_line(reply_token, result_message)
    else:
        reply_to_line(reply_token, "❌ AI ไม่สามารถแยกข้อมูลได้ รบกวนพิมพ์ใหม่อีกครั้งครับ")