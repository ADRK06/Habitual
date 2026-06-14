import tkinter as tk
import customtkinter as ctk
from datetime import date, timedelta
import habit_tracker as backend

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HabitualApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Habitual")
        self.geometry("450x700")
        self.resizable(False, False)
        
        self.db = backend.load_database()
        self.current_user = None
        
        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="#1B2838")
        self.container.pack(fill="both", expand=True)
        
        self.show_login_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_container()
        
        title = ctk.CTkLabel(self.container, text="🚀 HABIT REALM", font=("Helvetica", 24, "bold"))
        title.pack(pady=(80, 20))
        
        self.user_entry = ctk.CTkEntry(self.container, placeholder_text="Username", width=250)
        self.user_entry.pack(pady=10)
        
        self.pass_entry = ctk.CTkEntry(self.container, placeholder_text="Password", show="*", width=250)
        self.pass_entry.pack(pady=10)
        
        self.error_label = ctk.CTkLabel(self.container, text="", text_color="#ff6b6b")
        self.error_label.pack(pady=5)
        
        btn_login = ctk.CTkButton(self.container, text="Login", command=self.handle_login, width=250)
        btn_login.pack(pady=10)
        
        btn_reg = ctk.CTkButton(self.container, text="Create Profile", fg_color="transparent", border_width=1, command=self.handle_register, width=250)
        btn_reg.pack(pady=5)

    def handle_login(self):
        username = self.user_entry.get().strip().lower()
        password = self.pass_entry.get().strip()
        
        if username in self.db and self.db[username]["password"] == backend.hash_password(password):
            self.current_user = username
            self.show_dashboard_screen()
        else:
            self.error_label.configure(text="Invalid credentials!")

    def handle_register(self):
        username = self.user_entry.get().strip().lower()
        password = self.pass_entry.get().strip()
        
        if not username or len(password) < 4:
            self.error_label.configure(text="Password must be ≥ 4 chars!")
            return
        if username in self.db:
            self.error_label.configure(text="Username already taken!")
            return
            
        self.db[username] = {
            "password": backend.hash_password(password),
            "user_xp": 0,
            "user_level": 1,
            "habits": []
        }
        backend.save_database(self.db)
        self.error_label.configure(text="Account created! Please log in.", text_color="#2ecc71")

    def show_dashboard_screen(self):
        self.clear_container()
        user_data = self.db[self.current_user]
        
        # Header Info
        header = ctk.CTkFrame(self.container, height=100, fg_color="#0C447C")
        header.pack(fill="x", pady=(0, 15))
        
        welcome = ctk.CTkLabel(header, text=f"Welcome, {self.current_user.upper()}", font=("Helvetica", 18, "bold"), text_color="white")
        welcome.pack(pady=(10, 2))
        
        xp_needed = user_data["user_level"] * 100
        progress = user_data["user_xp"] / xp_needed
        
        lvl_lbl = ctk.CTkLabel(header, text=f"Level {user_data['user_level']} ({user_data['user_xp']}/{xp_needed} XP)", font=("Helvetica", 12), text_color="#B5D4F4")
        lvl_lbl.pack()
        
        xp_bar = ctk.CTkProgressBar(header, width=300)
        xp_bar.pack(pady=5)
        xp_bar.set(progress)

        # Scrollable Habit List Frame
        scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent", height=380)
        scroll_frame.pack(fill="both", expand=True, padx=15)

        active_habits = [h for h in user_data["habits"] if h.get("is_active", True)]
        
        if not active_habits:
            no_habits = ctk.CTkLabel(scroll_frame, text="No active habits yet. Add one below!", text_color="gray")
            no_habits.pack(pady=50)

        for h in active_habits:
            card = ctk.CTkFrame(scroll_frame, fg_color="#243447", border_width=1, border_color="#378ADD")
            card.pack(fill="x", pady=5, ipady=5)
            
            streak = backend.get_streak(h["date"])
            
            lbl_title = ctk.CTkLabel(card, text=h["name"].title(), font=("Helvetica", 15, "bold"), text_color="white")
            lbl_title.pack(anchor="w", padx=15, pady=(5, 0))
            
            lbl_streak = ctk.CTkLabel(card, text=f"🔥 {streak} days  |  🏆 Best: {h['best_streak']}", font=("Helvetica", 12), text_color="#B5D4F4")
            lbl_streak.pack(anchor="w", padx=15)
            
            # Action Buttons on Habit Card
            actions_frame = ctk.CTkFrame(card, fg_color="transparent")
            actions_frame.pack(fill="x", padx=15, pady=5)
            
            today = str(date.today())
            chk_text = "Completed Today ✅" if today in h["date"] else "Mark Complete"
            chk_state = "disabled" if today in h["date"] else "normal"
            
            btn_chk = ctk.CTkButton(actions_frame, text=chk_text, size=(120, 24), state=chk_state, 
                                    command=lambda h_ref=h: self.complete_habit(h_ref))
            btn_chk.pack(side="left", padx=(0, 10))
            
            btn_arc = ctk.CTkButton(actions_frame, text="Archive 📁", size=(80, 24), fg_color="#e67e22", 
                                    command=lambda h_ref=h: self.toggle_archive(h_ref))
            btn_arc.pack(side="right")

        # Bottom Menu Controller Bar
        nav_bar = ctk.CTkFrame(self.container, height=60, fg_color="#0e1722")
        nav_bar.pack(fill="x", side="bottom")
        
        ctk.CTkButton(nav_bar, text="+ New", width=90, command=self.show_add_popup).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(nav_bar, text="📊 Stats", width=90, command=self.show_stats_popup).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(nav_bar, text="Logout", width=90, fg_color="#c0392b", command=self.show_login_screen).pack(side="right", padx=10, pady=10)

    def complete_habit(self, habit):
        user_data = self.db[self.current_user]
        today = str(date.today())
        habit["date"].append(today)
        
        streak = backend.get_streak(habit["date"])
        if streak > habit["best_streak"]:
            habit["best_streak"] = streak
            
        user_data["user_xp"] += 15
        xp_needed = user_data["user_level"] * 100
        if user_data["user_xp"] >= xp_needed:
            user_data["user_xp"] -= xp_needed
            user_data["user_level"] += 1
            
        backend.save_database(self.db)
        self.show_dashboard_screen()

    def toggle_archive(self, habit):
        habit["is_active"] = False
        backend.save_database(self.db)
        self.show_dashboard_screen()

    def show_add_popup(self):
        dialog = ctk.CTkInputDialog(text="Enter new habit name:", title="Add Habit")
        name = dialog.get_input()
        if name:
            user_data = self.db[self.current_user]
            if any(h["name"].lower() == name.strip().lower() for h in user_data["habits"]):
                return
            user_data["habits"].append({"name": name.strip(), "date": [], "best_streak": 0, "is_active": True})
            backend.save_database(self.db)
            self.show_dashboard_screen()

    def show_stats_popup(self):
        user_data = self.db[self.current_user]
        total, best, worst = backend.calculate_analytics(user_data["habits"])
        
        popup = ctk.CTkToplevel(self)
        popup.title("Metrics Dashboard")
        popup.geometry("300x200")
        popup.attributes("-topmost", True)
        
        ctk.CTkLabel(popup, text="📈 INSIGHTS ENGINE", font=("Helvetica", 16, "bold")).pack(pady=15)
        ctk.CTkLabel(popup, text=f"Total Completions: {total}", font=("Helvetica", 13)).pack(pady=2)
        ctk.CTkLabel(popup, text=f"Best Day: {best}", font=("Helvetica", 13), text_color="#2ecc71").pack(pady=2)
        ctk.CTkLabel(popup, text=f"Vulnerable Day: {worst}", font=("Helvetica", 13), text_color="#e74c3c").pack(pady=2)

if __name__ == "__main__":
    app = HabitualApp()
    app.mainloop()