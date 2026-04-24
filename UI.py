import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tracker import ProgressTracker, BetweenSessionsStrategy


tracker = ProgressTracker(BetweenSessionsStrategy("weight"))

#Auto load
try:
    tracker.load_from_file("data.json")
except Exception as e:
    print("Load error", e)


root = tk.Tk()
root.title("Workout Tracker")
root.geometry("400x400")




def load_exercises(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print("Error loading", filename, e)
        return []

strength_exercises = load_exercises("C:/Users/danie/OneDrive/Desktop/kursinis/strength_exercises.txt")
cardio_exercises = load_exercises("C:/Users/danie/OneDrive/Desktop/kursinis/cardio_exercises.txt")
muscles = load_exercises("C:/Users/danie/OneDrive/Desktop/kursinis/muscles.txt")



def add_session_window():
    window = tk.Toplevel(root)
    window.title("Add Session")
    window.geometry("500x650")

    from workout import WorkoutSession, StrengthSet, CardioSet
    from exercise import StrengthExercise, CardioExercise

    tk.Label(window, text="Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(window)
    date_entry.pack()

    #Pasirinkimas: strength / cardio
    tk.Label(window, text="Set type").pack()
    set_type = tk.StringVar(value="strength")

    #Input laukai
    tk.Label(window, text="Exercise name").pack()
    exercise_var = tk.StringVar()
    exercise_dropdown = ttk.Combobox(window, textvariable=exercise_var, state="readonly")
    exercise_dropdown.pack()

    muscle_label = tk.Label(window, text="Muscle")
    muscle_var = tk.StringVar()
    muscle_dropdown = ttk.Combobox(window, textvariable=muscle_var, state="readonly")
    muscle_dropdown["values"] = muscles

    reps_label = tk.Label(window, text="Reps")
    reps_entry = tk.Entry(window)

    weight_label = tk.Label(window, text="Weight")
    weight_entry = tk.Entry(window)

    duration_label = tk.Label(window, text="Duration")
    duration_entry = tk.Entry(window)

    def update_fields():
        if set_type.get() == "strength":
            if not muscle_label.winfo_ismapped():
                muscle_label.pack()
                muscle_dropdown.pack()
                reps_label.pack()
                reps_entry.pack()
                weight_label.pack()
                weight_entry.pack()

            duration_label.pack_forget()
            duration_entry.pack_forget()

        else:
            if not duration_label.winfo_ismapped():
                duration_label.pack()
                duration_entry.pack()

            muscle_label.pack_forget()
            muscle_dropdown.pack_forget()
            reps_label.pack_forget()
            reps_entry.pack_forget()
            weight_label.pack_forget()
            weight_entry.pack_forget()
        
        if set_type.get() == "strength":
            exercise_dropdown["values"] = strength_exercises
        else:
            exercise_dropdown["values"] = cardio_exercises
        
        exercise_var.set("")


    exercise_var.set("")

    tk.Radiobutton(window, text="Strength", variable=set_type, value="strength", command=update_fields).pack()
    tk.Radiobutton(window, text="Cardio", variable=set_type, value="cardio", command=update_fields).pack()

    #Sarasas set'u
    sets_listbox = tk.Listbox(window, width=60)
    sets_listbox.pack(pady=10)

    #laikini set'ai
    temp_sets = []

    def add_set():
        try:
            name = exercise_var.get()

            if not name:
                raise ValueError("Select exercise")

            if set_type.get() == "strength":
                muscle = muscle_var.get()

                if not muscle:
                    raise ValueError("Select muscle")

                if not reps_entry.get() or not weight_entry.get():
                    raise ValueError("Reps and weight are required")
                
                reps = int(reps_entry.get())
                weight = float(weight_entry.get())

                ex = StrengthExercise(name, muscle)
                s = StrengthSet(ex, reps, weight)

            else:
                if not duration_entry.get():
                    raise ValueError("Duration is required")
                
                duration = float(duration_entry.get())

                ex = CardioExercise(name)
                s = CardioSet(ex, duration)
            
            temp_sets.append(s)
            sets_listbox.insert(tk.END, s.get_info())

            exercise_var.set("")
            muscle_var.set("")
            reps_entry.delete(0, tk.END)
            weight_entry.delete(0, tk.END)
            duration_entry.delete(0, tk.END)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    set_type.set("strength")
    update_fields()

    def save_session():
        try:
            date = date_entry.get()

            if not date:
                raise ValueError("Date is required")

            if not temp_sets:
                raise ValueError("Add at least one set")

            session = WorkoutSession(date)

            for s in temp_sets:
                session.add_set(s)
            
            tracker.add_workout_session(session)
            #Auto save
            tracker.save_to_file("data.json")

            window.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_set():
        try:
            selected = sets_listbox.curselection()

            if not selected:
                raise ValueError("Select a set to delete")
            
            index = selected[0]

            temp_sets.pop(index)

            sets_listbox.delete(index)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_set():
        try:
            selected = sets_listbox.curselection()

            if not selected:
                raise ValueError("Select a set to edit")
            
            index = selected[0]
            s = temp_sets[index]

            #Uzpildomai laukai
            exercise_var.set("")
            exercise_var.set(s.exercise.name)

            if isinstance(s, StrengthSet):
                set_type.set("strength")
                update_fields()

                muscle_var.set("")
                muscle_var.set(s.exercise.muscle)

                reps_entry.delete(0, tk.END)
                reps_entry.insert(0, s.reps)

                weight_entry.delete(0, tk.END)
                weight_entry.insert(0, s.weight)

            else:
                set_type.set("cardio")
                update_fields()

                duration_entry.delete(0, tk.END)
                duration_entry.insert(0, s.duration)
            
            #Istrinamas senas setas
            temp_sets.pop(index)
            sets_listbox.delete(index)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    
    tk.Button(window, text="Add set", command=add_set).pack(pady=5)
    tk.Button(window, text="Delete selected", command=delete_set).pack(pady=5)
    tk.Button(window, text="Edit selected", command=edit_set).pack(pady=5)
    tk.Button(window, text="Save session", command=save_session).pack(pady=10)
    tk.Button(window, text="Back", command=window.destroy).pack(pady=10)




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
    
    tk.Button(window, text="Back", command=window.destroy).pack(pady=10)




def calculate_progress_window():
    window = tk.Toplevel(root)
    window.title("Calculate Progress")
    window.geometry("400x400")

    tk.Label(window, text="Exercise name").pack()
    exercise_var = tk.StringVar()
    exercise_dropdown = ttk.Combobox(window, textvariable=exercise_var, state="readonly")
    exercise_dropdown.pack()

    result_label = tk.Label(window, text="")
    result_label.pack()

    #Tipas
    tk.Label(window, text="Type").pack()
    type_var = tk.StringVar(value="strength")

    def update_exercises():
        if type_var.get() == "strength":
            exercise_dropdown["values"] = strength_exercises
        else:
            exercise_dropdown["values"] = cardio_exercises

        exercise_var.set("")

    tk.Radiobutton(window, text="Strength", variable=type_var, value="strength", command=update_exercises).pack()
    tk.Radiobutton(window, text="Cardio", variable=type_var, value="cardio", command=update_exercises).pack()

    #Mode
    tk.Label(window, text="Mode").pack()
    mode_var = tk.StringVar(value="between")

    tk.Radiobutton(window, text="Between sessions", variable=mode_var, value="between").pack()
    tk.Radiobutton(window, text="Overall", variable=mode_var, value="overall").pack()

    update_exercises()

    def calculate():
        from tracker import BetweenSessionsStrategy, OverallStrategy

        try:
            name = exercise_var.get()

            if not name:
                raise ValueError("Enter exercise name")
            
            metric = "weight" if type_var.get() == "strength" else "duration"

            if mode_var.get() == "between":
                tracker.strategy = BetweenSessionsStrategy(metric)
            else:
                tracker.strategy = OverallStrategy(metric)

            result = tracker.calculate_progress(name)

            if isinstance(result, dict):
                result_label.config(
                    text=f"Best: {result['best']} | Last: {result['last']} | Progress: {result['progress']}"
                )
            else:
                result_label.config(text=f"Progress: {result}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Calculate", command=calculate).pack()
    tk.Button(window, text="Back", command=window.destroy).pack(pady=10)




def save_data():
    try:
        tracker.save_to_file("data.json")
        messagebox.showinfo("Saved", "Data saved successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))


#Buttons
tk.Button(root, text="Add workout session", command=add_session_window).pack(pady=10)
tk.Button(root, text="Show last sessions", command=show_sessions_window).pack(pady=10)
tk.Button(root, text="Calculate progress", command=calculate_progress_window).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

def run_app():
    root.mainloop()