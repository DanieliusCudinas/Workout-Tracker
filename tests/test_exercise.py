import unittest
from exercise import StrengthExercise, CardioExercise


class TestExercise(unittest.TestCase):

    def test_strength_exercise(self):
        ex = StrengthExercise("Bench Press", "Chest")

        self.assertEqual(ex.name, "Bench Press")
        self.assertEqual(ex.muscle, "Chest")

    def test_cardio_exercise(self):
        ex = CardioExercise("Running")

        self.assertEqual(ex.name, "Running")


if __name__ == "__main__":
    unittest.main()