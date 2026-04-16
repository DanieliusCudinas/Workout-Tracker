class Exersice:
    def __init__(self, name):
        self.name = name
    
    def get_info(self):
        return f"{self.name}"





class StrengthExercise(Exersice):
    def __init__(self, name, muscle):
        super().__init__(name)
        self.muscle = muscle
    
    def get_info(self):
        return f"{self.name} - {self.muscle}"




class CardioExercise(Exersice):
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



ex1 = StrengthExercise("Bench Press", "Chest")
ex2 = CardioExercise("Running", 30)

workout = WorkoutSession("2026-04-16")

session = WorkoutPlan("Kruitne ir Kardio")
session.add_exercise(ex1)
session.add_exercise(ex2)

session.show()