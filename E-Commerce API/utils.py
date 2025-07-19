from datetime import datetime

def validate_date(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None