import json
import requests
from groq import Groq
from src.core.config import logger, GROQ_API_KEY

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def transcribe_audio(audio_path: str) -> str:
    if not groq_client: return ""
    try:
        with open(audio_path, "rb") as file:
            return groq_client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model="whisper-large-v3",
                prompt="Transcribe Thai language accurately, including factory terms like ทินเนอร์, สีโป๊ว, กิ๊บ.",
                response_format="text",
                language="th"
            )
    except Exception as e:
        logger.error(f"Groq STT Error: {e}")
        return ""

def parse_requisition_text(transcript: str) -> dict:
    system_prompt = """
    You are a data extraction assistant for a Thai auto body shop. 
    Extract the employee name, material name, and quantity from the user's text.
    Return strictly a JSON object with keys: "employee_name", "item_name", "quantity".
    """
    payload = {
        "model": "scb10x/llama3.2-typhoon2-3b-instruct:latest",
        "prompt": f"{system_prompt}\n\nUser input: {transcript}",
        "stream": False,
        "format": "json"
    }
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        return json.loads(response.json()["response"])
    except Exception as e:
        logger.error(f"Ollama Parsing Error: {e}")
        return {}