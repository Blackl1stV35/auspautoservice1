from fastapi import FastAPI, Request, HTTPException
from src.config import logger
from src.ai_engine import run_ai_analysis
from src.etl_pipeline import run_etl_pipeline
import os

app = FastAPI(title="Auto Shop AI API")

@app.get("/")
def health_check():
    return {"status": "Online", "message": "API is running."}

@app.post("/trigger-etl")
def api_trigger_etl():
    """Endpoint to trigger the ETL process manually"""
    # Adjust paths based on your data folder location
    req_file = r"data\เอสพี--สถิติเบิกวัสดุสิ้นเปลือง(69).xlsx"
    pur_file = r"data\3--เอสพี--ต้นทุนแผนกสี และน้ำมัน และกิ๊บน๊อต.xlsx"
    
    try:
        run_etl_pipeline(req_file, pur_file)
        run_ai_analysis()
        return {"status": "Success", "message": "Pipeline and AI analysis executed."}
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Placeholder for LINE Webhook
@app.post("/webhook")
async def line_webhook(request: Request):
    """
    Future implementation for LINE Bot interactions.
    Employees can send 'เบิก กระดาษทราย 5' and it will insert via db_operations.py
    """
    body = await request.body()
    # verify signature & parse events here
    return 'OK'