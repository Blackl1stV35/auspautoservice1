from src.core.config import supabase, logger

_employee_cache = {}
_material_cache = {}

def get_or_create_employee(name: str) -> int:
    name = str(name).strip()
    if name in _employee_cache: return _employee_cache[name]
        
    res = supabase.table("employees").select("id").eq("name", name).execute()
    if res.data:
        emp_id = res.data[0]['id']
    else:
        new_res = supabase.table("employees").insert({"name": name}).execute()
        emp_id = new_res.data[0]['id']
        
    _employee_cache[name] = emp_id
    return emp_id

def get_or_create_material(name: str) -> int:
    name = str(name).strip()
    if name in _material_cache: return _material_cache[name]
        
    res = supabase.table("materials").select("id").eq("item_name", name).execute()
    if res.data:
        mat_id = res.data[0]['id']
    else:
        new_res = supabase.table("materials").insert({"item_name": name}).execute()
        mat_id = new_res.data[0]['id']
        
    _material_cache[name] = mat_id
    return mat_id

def batch_insert(table_name: str, data: list, batch_size: int = 500):
    if not data: return
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        try:
            supabase.table(table_name).insert(batch).execute()
            logger.info(f"Inserted {len(batch)} rows into {table_name}")
        except Exception as e:
            logger.error(f"Failed to insert into {table_name}: {e}")