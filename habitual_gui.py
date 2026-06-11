import customtkinter as ctk

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
root.mainloop()