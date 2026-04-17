class ProgressTracker:
    def __init__(self, strategy):
        self.workout_sessions = []
        self.strategy = strategy

    def add_workout_session(self, session):
        self.workout_sessions.append(session)

    def calculate_progress(self, exercise_name):
        return self.strategy.calculate(self.workout_sessions, exercise_name)





class ProgressStrategy:
    def calculate(self, sessions, exercise_name):
        raise NotImplementedError("Each strategy must implement calculate method")





class StrengthProgressStrategy(ProgressStrategy):
    def calculate(self, sessions, exercise_name):
        if len(sessions) < 2:
            return None
        
        def get_max_weight(session):
            max_weight = 0
            for s in session.sets:
                if s.exercise.name == exercise_name:
                    if s.weight > max_weight:
                        max_weight = s.weight
            return max_weight
        
        session_1 = get_max_weight(sessions[-2])
        session_2 = get_max_weight(sessions[-1])

        return session_2 - session_1





class CardioProgressStrategy(ProgressStrategy):
    def calculate(self, sessions, exercise_name):
        if len(sessions) < 2:
            return None
        
        def get_max_duration(session):
            max_duration = 0
            for s in session.sets:
                if s.exercise.name == exercise_name:
                    if s.duration > max_duration:
                        max_duration = s.duration
            return max_duration
        
        session_1 = get_max_duration(sessions[-2])
        session_2 = get_max_duration(sessions[-1])

        return session_2 - session_1