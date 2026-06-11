import json
from datetime import date , timedelta

def show_menu():
    print("\n----HABIT TRACKER----")
    print("1. Add a new habit")
    print("2. Mark habit as completed")
    print("3. View all habits")
    print("4. Delete a habit")  
    print("5. Exit\n")

def load_habits():
        try:
            with open("habits.json","r") as f:
                content = f.read()
                if not content:
                    return []
                return json.loads(content)
        except FileNotFoundError:
            return []

habits = load_habits()

def save_habits():
        with open("habits.json","w") as f:
            json.dump(habits,f)

def get_streak(dates):
    count = 0
    chk = date.today()
    while str(chk) in dates:
        count+=1
        chk -= timedelta(days=1)
    return count

def main():
    
    while True:
        show_menu()
        choice = input("Enter your choice: ")
    
        if choice == '1':
            print("\n")
            habit=input("Enter new habit: ( 0 to return )  ")
            if habit == '0':
                continue
            if habit.strip() == "":
                print("Habit name cannot be empty.")
                continue
            if any(h["name"].lower() == habit.lower() for h in habits):
                print("Habit already exists.")
                continue
            habits.append({"name":habit,"date":[],"best_streak":0})
            save_habits()
            print(f"{habit} added to your habit list.")
        
        elif choice == '2':
            print("\n")
            if len(habits) == 0:
                print("No habits to mark as completed.")
            else:
                print("Select a habit to mark as completed:")
                for i,habit in enumerate(habits,start=1):
                    print(f"{i}. {habit['name']}")
                pick = int(input("Enter habit number: ( 0 to return )"))
                if pick == '0':
                    continue
                if pick < 1 or pick > len(habits):
                    print("Invalid habit number.")
                    continue
                picked_habit = habits[pick-1]
                today = str(date.today())
                if today in picked_habit["date"]:
                    print("You have already marked this as completed today.")
                else:
                    picked_habit["date"].append(today)
                    streak = get_streak(picked_habit["date"])
                    if streak > picked_habit["best_streak"]:
                        picked_habit["best_streak"] = streak 
                    save_habits()
                    print(f"{picked_habit['name']} marked completed!")

        elif choice == '3':
            print("\n")
            if len(habits) == 0:
                print("No habits to show.")
            else:
                print("Your habits:")
                today = date.today()
                monday = today - timedelta(days=today.weekday())
                week_days = [monday + timedelta(days=i) for i in range(7)]
                for i,habit in enumerate(habits, start=1):
                    streak = get_streak(habit["date"])
                    print(f"{i}. {habit['name']} - 🔥 {streak} day streak | best: {habit['best_streak']}")
                    week_display = ""
                    day_names=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
                    for i,day in enumerate(week_days):
                        mark = "✅" if str(day) in habit["date"] else "❌"
                        week_display += f"{day_names[i]} {mark} "
                    print(f" {week_display}")

        elif choice == '4':
            print("\n")
            if len(habits) == 0:
                print("No habits to delete.")
            else:
                print("Select a habit to delete: ( 0 to return )")
                for i,habit in enumerate(habits,start=1):
                    print(f"{i}. {habit['name']}")
                pick = int(input("Enter habit number:"))
                if pick == 0:
                    continue
                if pick < 1 or pick > len(habits):
                    print("Invalid habit number.")
                    continue
                deleted_habit = habits.pop(pick-1)
                save_habits()
                print(f"{deleted_habit['name']} deleted.")

        elif choice == '5':
            print("\n")
            print("Exiting the habit tracker. Goodbye!")
            break
       
        else:
            print("\n")
            print("Invalid choice. Please try again.")

main()