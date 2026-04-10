# reset_db.py
from src.core.config import supabase, logger

def safe_delete(table_name):
    try:
        supabase.table(table_name).delete().neq("id", 0).execute()
        print(f"✅ Cleared table: {table_name}")
    except Exception as e:
        print(f"⚠️ Could not clear '{table_name}' (It might not exist yet). Skipping...")

def clear_database():
    print("⚠️ Wiping database for ETL refresh...")
    # Order matters! Child tables first to prevent foreign key relation errors.
    tables_to_clear = ["ai_insights", "transactions", "purchases", "materials", "employees"]
    
    for table in tables_to_clear:
        safe_delete(table)
        
    print("🎉 Database reset sequence complete! You can now run the ETL pipeline.")

if __name__ == "__main__":
    clear_database()