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





class BetweenSessionsStrengthProgressStrategy(ProgressStrategy):
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




class OverallStrenghtProgressStrategy(ProgressStrategy):
    def calculate(self, sessions, exercise_name):
        if len(sessions) < 2:
            return None
        
        def get_max_weight(session):
            max_weight = 0
            found = False

            for s in session.sets:
                if s.exercise.name == exercise_name:
                    found = True
                    if s.weight > max_weight:
                        max_weight = s.weight

            return max_weight, found
        

        #didziausias max per visas treniruotes, isskirus paskutine
        max_overall = 0
        found_any = False

        for session in sessions[:-1]:
            session_max, found = get_max_weight(session)

            if found:
                found_any = True
                if session_max > max_overall:
                    max_overall = session_max
        
        #paskutines treniruotes max
        last_max, found_last = get_max_weight(sessions[-1])

        if not found_any:
            return None
        
        if not found_last:
            return None
        
        return last_max - max_overall




class BetweenSessionsCardioProgressStrategy(ProgressStrategy):
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




class OverallCardioProgressStrategy(ProgressStrategy):
    def calculate(self, sessions, exercise_name):
        if len(sessions) < 2:
            return None
        
        def get_max_duration(session):
            max_duration = 0
            found = False

            for s in session.sets:
                if s.exercise.name == exercise_name:
                    found = True
                    if s.duration > max_duration:
                        max_duration = s.duration

            return max_duration, found
        

        #didziausias max per visas treniruotes, isskirus paskutine
        max_overall = 0
        found_any = False

        for session in sessions[:-1]:
            session_max, found = get_max_duration(session)

            if found:
                found_any = True
                if session_max > max_overall:
                    max_overall = session_max
        
        #paskutines treniruotes max
        last_max, found_last = get_max_duration(sessions[-1])

        if not found_any:
            return None
        
        if not found_last:
            return None
        
        return last_max - max_overall