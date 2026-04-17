class Exercise:
    def __init__(self, name):
        self.name = name
    
    def get_info(self):
        return f"{self.name}"





class StrengthExercise(Exercise):
    def __init__(self, name, muscle):
        super().__init__(name)
        self.muscle = muscle
    
    def get_info(self):
        return f"{self.name} - {self.muscle}"




class CardioExercise(Exercise):
    def __init__(self, name, duration):
        super().__init__(name)
        self.duration = duration
    
    def get_info(self):
        return f"{self.name} - {self.duration}"





class WorkoutPlan:
    def __init__(self, name):
        self.name = name
        self.exercises = []

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def show(self):
        print(f"\nPlanas: {self.name}")
        for ex in self.exercises:
            print("-", ex.get_info())




class Set:
    def __init__(self, exercise, reps, weight):
        self.exercise = exercise
        self.reps = reps
        self.weight = weight

    def get_info(self):
        return f"{self.exercise.name}: {self.reps} reps x {self.weight} kg"




class WorkoutSession:
    def __init__(self, date):
        self.date = date
        self.sets = []

    def add_set(self, set_obj):
        self.sets.append(set_obj)

    def show(self):
        print(f"\nTreniruotė: {self.date}")
        for s in self.sets:
            print("-", s.get_info())




class ProgressTracker:
    def __init__(self):
        self.workout_sessions = []

    def add_workout_session(self, session):
        self.workout_sessions.append(session)
    
    def track_weight(self, exercise_name):
        max_weight = 0

        for session in self.workout_sessions:
            for s in session.sets:
                if s.exercise.name == exercise_name:
                    if s.weight > max_weight:
                        max_weight = s.weight
        
        return max_weight
    
    def between_session_weight_result(self, exercise_name):
        if len(self.workout_sessions) >= 2:

            max_weight_1 = 0
            for s in self.workout_sessions[len(self.workout_sessions)-2].sets:
                    if s.exercise.name == exercise_name:
                        if s.weight > max_weight_1:
                            max_weight_1 = s.weight

            max_weight_2 = 0
            for s in self.workout_sessions[len(self.workout_sessions)-1].sets:
                    if s.exercise.name == exercise_name:
                        if s.weight > max_weight_2:
                            max_weight_2 = s.weight
        
            return max_weight_2 - max_weight_1
    
        else: 
            return None