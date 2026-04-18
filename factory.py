from tracker import (
    ProgressTracker,
    BetweenSessionsStrengthProgressStrategy,
    OverallStrenghtProgressStrategy,
    BetweenSessionsCardioProgressStrategy,
    OverallCardioProgressStrategy
)


class TrackerFactory:
    # possible exercise_type = strength, cardio
    # possible mode = between, overall
    @staticmethod
    def create_tracker(exercise_type, mode):
        strategy = None
        
        if exercise_type == "strength":
            if mode == "between":
                strategy = BetweenSessionsStrengthProgressStrategy()
            elif mode == "overall":
                strategy = OverallStrenghtProgressStrategy()
            else:
                raise ValueError("Invalid mode")

        elif exercise_type == "cardio":
            if mode == "between":
                strategy = BetweenSessionsCardioProgressStrategy()
            elif mode == "overall":
                strategy = OverallCardioProgressStrategy()
            else:
                raise ValueError("Invalid mode")
        
        else:
            raise ValueError("Invalid exercise type")
        
        tracker = ProgressTracker(strategy)

        return tracker