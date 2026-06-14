import json
import hashlib
from datetime import date, timedelta

DB_FILE = "habits.json"

def load_database():
    try:
        with open(DB_FILE, "r") as f:
            content = f.read()
            if not content: return {}
            data = json.loads(content)
            if isinstance(data, list): return {}  # Reset if old schema
            return data
    except FileNotFoundError:
        return {}

def save_database(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_streak(dates):
    count = 0
    chk = date.today()
    if str(chk) not in dates:
        chk -= timedelta(days=1)
    while str(chk) in dates:
        count += 1
        chk -= timedelta(days=1)
    return count

def calculate_analytics(habits):
    active_habits = [h for h in habits if h.get("is_active", True)]
    total_completions = sum(len(h["date"]) for h in active_habits)
    day_counts = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    
    for habit in active_habits:
        for d_str in habit["date"]:
            try:
                yr, mo, dy = map(int, d_str.split('-'))
                day_name = date(yr, mo, dy).strftime("%A")
                day_counts[day_name] += 1
            except ValueError:
                continue
                
    best_day = max(day_counts, key=day_counts.get) if total_completions > 0 else "N/A"
    worst_day = min(day_counts, key=day_counts.get) if total_completions > 0 else "N/A"
    return total_completions, best_day, worst_day