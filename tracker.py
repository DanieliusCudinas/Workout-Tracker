import json


class ProgressTracker:
    def __init__(self, strategy):
        self.workout_sessions = []
        self.strategy = strategy

    def add_workout_session(self, session):
        self.workout_sessions.append(session)

    def calculate_progress(self, exercise_name):
        return self.strategy.calculate(self.workout_sessions, exercise_name)
    
    def save_to_file(self, filename):
        data = [session.to_dict() for session in self.workout_sessions]

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    
    def load_from_file(self, filename):
        from workout import WorkoutSession, StrengthSet, CardioSet
        from exercise import StrengthExercise, CardioExercise

        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File not found")
            return
        except json.JSONDecodeError:
            print("Invalid JSON format")
            return

        with open(filename, "r") as f:
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

        if not found_prev and not found_last:
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
        max_overall = 0
        found_any = False

        for session in sessions[:-1]:
            session_max, found = get_max_value(session)

            if found:
                found_any = True
                if session_max > max_overall:
                    max_overall = session_max
        
        #paskutines treniruotes max
        last_max, found_last = get_max_value(sessions[-1])

        if not found_any and not found_last:
            raise ValueError("Exercise not found")
        
        return last_max - max_overall