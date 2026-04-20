import json
import os


class ProgressTracker:
    def __init__(self, strategy):
        self.workout_sessions = []
        self.strategy = strategy

    def add_workout_session(self, session):
        self.workout_sessions.append(session)

    def calculate_progress(self, exercise_name):
        return self.strategy.calculate(self.workout_sessions, exercise_name)
    
    def save_to_file(self, filename):
        base_dir = os.path.dirname(__file__)

        filepath = os.path.join(base_dir, filename)

        data = [session.to_dict() for session in self.workout_sessions]

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Saved to: {filepath}")
    
    def load_from_file(self, filename):
        from workout import WorkoutSession, StrengthSet, CardioSet
        from exercise import StrengthExercise, CardioExercise

        base_dir = os.path.dirname(__file__)
        filepath = os.path.join(base_dir, filename)
        
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File not found")
            return
        except json.JSONDecodeError:
            print("Invalid JSON format")
            return

        with open(filepath, "r") as f:
            data = json.load(f)
        
        self.workout_sessions = []

        for session_data in data:
            session = WorkoutSession(session_data["date"])

            for s in session_data["sets"]:
                if s["type"] == "strength":
                    exercise = StrengthExercise(s["name"], s["muscle"])
                    set_obj = StrengthSet(exercise, s["reps"], s["weight"])
                
                elif s["type"] == "cardio":
                    exercise = CardioExercise(s["name"])
                    set_obj = CardioSet(exercise, s["duration"])

                else:
                    raise ValueError(f"Unknown set type: {s['type']}")

                session.add_set(set_obj)

            self.workout_sessions.append(session)
        
        print(f"Loaded from: {filepath}")
    
    def get_last_sessions(self, n=5):
        if n <= 0:
            return []
        return self.workout_sessions[-n:]
    
    def show_last_sessions(self, n=5):
        sessions = self.get_last_sessions(n)

        if not sessions:
            print("No sessions found")
            return
        
        print(f"\nShowing last {len(sessions)} sessions:\n")

        for session in sessions:
            session.show()




class ProgressStrategy:
    def calculate(self, sessions, exercise_name):
        raise NotImplementedError("Each strategy must implement calculate method")




class BetweenSessionsStrategy(ProgressStrategy):
    def __init__(self, metric):
        self.metric = metric

    def calculate(self, sessions, exercise_name):
        if len(sessions) < 2:
            return None
        
        def get_max_value(session):
            max_value = 0
            found = False
            for s in session.sets:
                if s.exercise.name == exercise_name:
                    found = True
                    value = getattr(s, self.metric, None)
                    if value is not None and value > max_value:
                        max_value = value

            return max_value, found       
        
        previous_max, found_prev = get_max_value(sessions[-2])
        last_max, found_last = get_max_value(sessions[-1])

        if not found_prev or not found_last:
            raise ValueError("Exercise not found")

        return last_max - previous_max




class OverallStrategy(ProgressStrategy):
    def __init__(self, metric):
        self.metric = metric

    def calculate(self, sessions, exercise_name):
        if len(sessions) < 2:
            return None
        
        def get_max_value(session):
            max_value = 0
            found = False

            for s in session.sets:
                if s.exercise.name == exercise_name:
                    found = True
                    value = getattr(s, self.metric, None)
                    if value is not None and value > max_value:
                        max_value = value

            return max_value, found
        

        #didziausias max per visas treniruotes, isskirus paskutine
        best_overall = None
        found_any = False

        for session in sessions[:-1]:
            session_max, found = get_max_value(session)

            if found:
                found_any = True
                if best_overall is None or session_max > best_overall:
                    best_overall = session_max
        
        #paskutines treniruotes max
        last_max, found_last = get_max_value(sessions[-1])

        if not found_any or not found_last:
            raise ValueError("Exercise not found")
        
        progress = last_max - best_overall

        if progress > 0:
            status = "Improved"
        elif progress < 0:
            status = "Decreased"
        else:
            status = "Same"

        return {
            "best": best_overall,
            "last": last_max,
            "progress": progress,
            "status": status
        }