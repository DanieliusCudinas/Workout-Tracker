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

    @property
    def reps(self):
        return self._reps
    
    @reps.setter
    def reps(self, value):
        if value is None or value < 0:
            raise ValueError("Reps cannot be empty / cannot be less than 0")
        self._reps = value

    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, value):
        if value is None or value < 0:
            raise ValueError("Weight cannot be empty / cannot be less than 0")
        self._weight = value

    def get_info(self):
        return f"{self.exercise.name}: {self.reps} reps x {self.weight} kg"
    
    def to_dict(self):
        return {
            "type": "strength",
            "name": self.exercise.name,
            "muscle": self.exercise.muscle,
            "reps": self.reps,
            "weight": self.weight
        }



class CardioSet(Set):
    def __init__(self, exercise, duration):
        super().__init__(exercise)
        self.duration = duration

    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, value):
        if value is None or value < 0:
            raise ValueError("Duration cannot be empty / cannot be less than 0")
        self._duration = value
    
    def get_info(self):
        return f"{self.exercise.name}: {self.duration} min"
    
    def to_dict(self):
        return {
            "type": "cardio",
            "name": self.exercise.name,
            "duration": self.duration
        }
    



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
    
    def to_dict(self):
        return {
            "date": self.date,
            "sets": [s.to_dict() for s in self.sets]
        }