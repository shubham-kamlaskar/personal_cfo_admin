def generate_client_id(emp_count: int) -> str:
    base_code = "2600"
    sequence = str(emp_count + 1).zfill(3)   # 001, 002, 003
    return sequence