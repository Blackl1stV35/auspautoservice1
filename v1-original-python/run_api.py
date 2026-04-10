import uvicorn

if __name__ == "__main__":
    print("🌐 Starting Auto Shop LINE API Server...")
    # Points to the app inside src/api/bot.py
    uvicorn.run("src.api.bot:app", host="0.0.0.0", port=8000, reload=True)