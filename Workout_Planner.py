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