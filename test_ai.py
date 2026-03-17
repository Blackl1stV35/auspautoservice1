# test_ai.py
import logging
from src.ai_engine import run_ai_analysis

# Setup basic console logging so we can see the AI's output
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

if __name__ == "__main__":
    print("🚀 Booting up the Machine Learning Engine...")
    print("-------------------------------------------------")
    
    try:
        run_ai_analysis()
        print("-------------------------------------------------")
        print("✅ AI Analysis Complete! Check the terminal for Anomalies or Forecasts.")
    except Exception as e:
        print(f"❌ Error running AI: {e}")