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
        

        found_sessions = []

        for session in reversed(sessions):
            max_value, found = get_max_value(session)
            if found:
                found_sessions.append(max_value)
            if len(found_sessions) == 2:
                break
        
        if len(found_sessions) < 2:
            return "Not enough data"
        
        return found_sessions[0] - found_sessions[1]




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
        

        best_overall = None
        last_value = None

        for session in reversed(sessions):
            session_max, found = get_max_value(session)

            if found:
                if last_value is None:
                    last_value = session_max
                else:
                    if best_overall is None or session_max > best_overall:
                        best_overall = session_max

        if last_value is None:
            return "Exercise never done"

        if best_overall is None:
            return "Only one data point"

        progress = last_value - best_overall

        status = "Improved" if progress > 0 else "Decreased" if progress < 0 else "Same"

        return {
            "best": best_overall,
            "last": last_value,
            "progress": progress,
            "status": status
        }