import json
from datetime import date, timedelta
import customtkinter as ctk

def load_habits():
    try:
        with open("habits.json","r") as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []

def get_streak(dates):
    count = 0
    chk = date.today()
    while str(chk) in dates:
        count +=1
        chk -= timedelta(days=1)
    return count

habits = load_habits() 

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Habitual")
root.geometry("400x600")
root.resizable(False, False)

import tkinter as tk

header = tk.Canvas(root, bg="#0C447C", height=80, highlightthickness=0)
header.pack(fill="x")
header.create_text(200, 40, text="Habitual", font=("Helvetica", 24, "bold"), fill="white")

content = ctk.CTkFrame(root, fg_color="#1B2838", corner_radius=0)
content.pack(fill="both", expand=True)


stats_bar = tk.Canvas(root, bg="#185FA5", height=50, highlightthickness=0)
stats_bar.pack(fill="x")
stats_bar.create_text(100, 25, text="3 habits", font=("Helvetica", 13), fill="white")
stats_bar.create_text(280, 25, text="🔥 1 active streak", font=("Helvetica", 13),fill="white")


day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
today = date.today()
monday = today - timedelta(days=today.weekday())
week_days = [monday + timedelta(days=i) for i in range(7)]

for habit in habits:
    card = tk.Canvas(content, bg="white", height=100, highlightthickness=1, highlightbackground="#B5D4F4")
    card.pack(fill="x", padx=15, pady=8)

    streak = get_streak(habit["date"])

    week_display = ""
    for i, day in enumerate(week_days):
        mark = "✅" if str(day) in habit["date"] else "❌"
        week_display += f"{day_names[i]}{mark} "

    card.create_text(20, 20, text=habit["name"],  font=("Helvetica", 14, "bold"), fill="#0C447C", anchor="w")
    card.create_text(20, 45, text=f"🔥 {streak} day streak  |  best: {habit['best_streak']}", font=("Helvetica", 11), fill="#378ADD", anchor="w")
    card.create_text(20, 75, text=week_display, font=("Helvetica", 11), fill="#185FA5", anchor="w")

root.mainloop()