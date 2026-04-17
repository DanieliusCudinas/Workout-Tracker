from exercise import Exercise

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
    def __init__(self, exercise):
        self.exercise = exercise




class StrengthSet(Set):
    def __init__(self, exercise, reps, weight):
        super().__init__(exercise)
        self.reps = reps
        self.weight = weight




class CardioSet(Set):
    def __init__(self, exercise, duration):
        super().__init__(exercise)
        self.duration = duration
    



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