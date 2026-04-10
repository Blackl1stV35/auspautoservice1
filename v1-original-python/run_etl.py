import time
from src.workers.etl import run_etl_pipeline

if __name__ == "__main__":
    print("🚀 Starting High-Performance ETL Pipeline...")
    start_time = time.time()
    
    req_file = r"data\เอสพี--สถิติเบิกวัสดุสิ้นเปลือง(69).xlsx"
    pur_file = r"data\3--เอสพี--ต้นทุนแผนกสี และน้ำมัน และกิ๊บน๊อต.xlsx"
    
    run_etl_pipeline(req_file, pur_file)
    
    print(f"✅ ETL Complete! Finished in {round(time.time() - start_time, 2)} seconds.")