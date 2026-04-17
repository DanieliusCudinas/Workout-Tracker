import unittest

from exercise import StrengthExercise
from workout import Set, WorkoutSession
from tracker import ProgressTracker


class TestProgressTracker(unittest.TestCase):

    def test_track_weight(self):
        # Sukuriam pratimą
        bench = StrengthExercise("Bench Press", "Chest")

        # Sukuriam treniruotę
        session = WorkoutSession("2026-04-10")
        session.add_set(StrengthSet(bench, 8, 80))
        session.add_set(StrengthSet(bench, 6, 90))

        # Tracker
        #tracker = ProgressTracker()
        #tracker.add_workout_session(session)

        # Testuojam
        #result = tracker.track_weight("Bench Press")

        # Tikrinam ar teisinga
        #self.assertEqual(result, 90)


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



#STRENGTH PROGRESS TEST

from tracker import (
    ProgressTracker,
    StrengthProgressStrategy,
    CardioProgressStrategy
)

from workout import WorkoutSession, Set, StrengthSet, CardioSet
from exercise import StrengthExercise, CardioExercise

class TestStrengthProgress(unittest.TestCase):

    def test_strength_progress(self):
        bench = StrengthExercise("Bench Press", "Chest")

        session1 = WorkoutSession("2026-04-10")
        session1.add_set(StrengthSet(bench, 8, 80))

        session2 = WorkoutSession("2026-04-12")
        session2.add_set(StrengthSet(bench, 6, 90))

        tracker = ProgressTracker(StrengthProgressStrategy())
        tracker.add_workout_session(session1)
        tracker.add_workout_session(session2)

        result = tracker.calculate_progress("Bench Press")

        self.assertEqual(result, 10)




# CARDIO PROGRESS TEST

class TestCardioProgress(unittest.TestCase):

    def test_cardio_progress(self):
        running = CardioExercise("Running", 30)

        session1 = WorkoutSession("2026-04-10")
        session1.add_set(CardioSet(running, 30))

        session2 = WorkoutSession("2026-04-12")
        session2.add_set(CardioSet(running, 40))

        tracker = ProgressTracker(CardioProgressStrategy())
        tracker.add_workout_session(session1)
        tracker.add_workout_session(session2)

        result = tracker.calculate_progress("Running")

        self.assertEqual(result, 10)