import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from exercise import StrengthExercise
from workout import Set, WorkoutSession
from tracker import ProgressTracker


class TestProgressTracker(unittest.TestCase):

    def test_track_weight(self):
        # Sukuriam pratimą
        bench = StrengthExercise("Bench Press", "Chest")

        # Sukuriam treniruotę
        session = WorkoutSession("2026-04-10")
        session.add_set(Set(bench, 8, 80))
        session.add_set(Set(bench, 6, 90))

        # Tracker
        tracker = ProgressTracker()
        tracker.add_workout_session(session)

        # Testuojam
        result = tracker.track_weight("Bench Press")

        # Tikrinam ar teisinga
        self.assertEqual(result, 90)


if __name__ == "__main__":
    unittest.main()

def test_between_session_weight(self):
    # Sukuriam pratimą
    bench = StrengthExercise("Bench Press", "Chest")

    # Pirma treniruotė
    session1 = WorkoutSession("2026-04-10")
    session1.add_set(Set(bench, 8, 80))

    # Antra treniruotė
    session2 = WorkoutSession("2026-04-12")
    session2.add_set(Set(bench, 6, 90))

    # Tracker
    tracker = ProgressTracker()
    tracker.add_workout_session(session1)
    tracker.add_workout_session(session2)

    # Testuojam progresą
    result = tracker.between_session_weight_result("Bench Press")

    # Tikrinam
    self.assertEqual(result, 10)