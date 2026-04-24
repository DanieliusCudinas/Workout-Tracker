import unittest
from tracker import ProgressTracker, BetweenSessionsStrategy, OverallStrategy
from workout import WorkoutSession, StrengthSet
from exercise import StrengthExercise


class TestProgressTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = ProgressTracker(BetweenSessionsStrategy("weight"))

        # Sukuriam 2 session
        ex = StrengthExercise("Bench Press", "Chest")

        s1 = WorkoutSession("2024-01-01")
        s1.add_set(StrengthSet(ex, 10, 50))

        s2 = WorkoutSession("2024-01-02")
        s2.add_set(StrengthSet(ex, 10, 60))

        self.tracker.add_workout_session(s1)
        self.tracker.add_workout_session(s2)

    def test_between_sessions_progress(self):
        result = self.tracker.calculate_progress("Bench Press")
        self.assertEqual(result, 10)

    def test_overall_progress(self):
        self.tracker.strategy = OverallStrategy("weight")
        result = self.tracker.calculate_progress("Bench Press")

        self.assertEqual(result["progress"], 10)
        self.assertEqual(result["best"], 50)
        self.assertEqual(result["last"], 60)


if __name__ == "__main__":
    unittest.main()