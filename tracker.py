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




class BetweenSessionsStrategy(ProgressStrategy):
    def __init__(self, metric):
        self.metric = metric

    def calculate(self, sessions, exercise_name):
        if len(sessions) < 2:
            return None
        
        def get_max_value(session):
            max_value = 0
            flag = False
            for s in session.sets:
                if s.exercise.name == exercise_name:
                    flag = True
                    value = getattr(s, self.metric, None)
                    if value is not None and value > max_value:
                        max_value = value

            return max_value, flag
        
        previous_max, found = get_max_value(sessions[-2])
        if not found:
            raise ValueError("Exercise not found")
        
        last_max, found = get_max_value(sessions[-1])
        if not found:
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