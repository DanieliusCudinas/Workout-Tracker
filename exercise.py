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