import unittest
from workout import WorkoutSession, StrengthSet
from exercise import StrengthExercise


class TestWorkoutSession(unittest.TestCase):

    def test_add_set(self):
        session = WorkoutSession("2024-01-01")
        ex = StrengthExercise("Squat", "Legs")
        s = StrengthSet(ex, 8, 80)

        session.add_set(s)

        self.assertEqual(len(session.sets), 1)
        self.assertEqual(session.sets[0].exercise.name, "Squat")


if __name__ == "__main__":
    unittest.main()