import tkinter as tk
from tracker import ProgressTracker, BetweenSessionsStrategy


tracker = ProgressTracker(BetweenSessionsStrategy("weight"))

#Auto load
try:
    tracker.load_from_file("data.json")
except Exception:
    pass


root = tk.Tk()
root.title("Workout Tracker")
root.geometry("400x400")


def add_session_window():
    window = tk.Toplevel(root)
    window.title("Add Session")
    window.geometry("400x400")

    tk.Label(window, text="Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(window)
    date_entry.pack()

    def save_session():
        from workout import WorkoutSession

        date = date_entry.get()
        session = WorkoutSession(date)

        tracker.add_workout_session(session)
        print("Session added")
    
    tk.Button(window, text="Save session", command=save_session).pack(pady=10)




def show_sessions_window():
    window = tk.Toplevel(root)
    window.title("Sessions")

    text = tk.Text(window, width=50, height=20)
    text.pack()

    sessions = tracker.get_last_sessions(10)

    if not sessions:
        text.insert(tk.END, "No sessions found\n")
        return
    
    for session in sessions:
        text.insert(tk.END, f"\nDate: {session.date}\n")
        for s in session.sets:
            text.insert(tk.END, f" - {s.get_info()}\n")




def calculate_progress_window():
    window = tk.Toplevel(root)
    window.title("Calculate Progress")

    tk.Label(window, text="Exercise name").pack()
    entry = tk.Entry(window)
    entry.pack()

    result_label = tk.Label(window, text="")
    result_label.pack()

    def calculate():
        from tracker import BetweenSessionsStrategy, OverallStrategy

        tracker.strategy = BetweenSessionsStrategy("weight")

        try:
            result = tracker.calculate_progress(entry.get())

            if isinstance(result, dict):
                result_label.config(
                    text=f"Best: {result['best']} | Last: {result['last']} | Progress: {result['progress']}"
                )
            else:
                result_label.config(text=f"Progress: {result}")

        except Exception as e:
            result_label.config(text=f"Error: {e}")

    tk.Button(window, text="Calculate", command=calculate).pack()




def save_data():
    tracker.save_to_file("data.json")
    print("SAVED")


#Buttons
tk.Button(root, text="Add workout session", command=add_session_window).pack(pady=10)
tk.Button(root, text="Show last sessions", command=show_sessions_window).pack(pady=10)
tk.Button(root, text="Calculate progress", command=calculate_progress_window).pack(pady=10)
tk.Button(root, text="Save", command=save_data).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)


root.mainloop()