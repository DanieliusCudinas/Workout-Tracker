from exercise import StrengthExercise, CardioExercise
from workout import WorkoutSession, StrengthSet, CardioSet
from tracker import ProgressTracker, StrengthProgressStrategy, CardioProgressStrategy


if __name__ == "__main__":

    # Pratimai
    bench = StrengthExercise("Bench Press", "Chest")
    squat = StrengthExercise("Squat", "Legs")
    running = CardioExercise("Running", 30)


    # Pirma treniruote
    session1 = WorkoutSession("2026-04-10")
    session1.add_set(StrengthSet(bench, 8, 80))
    session1.add_set(StrengthSet(squat, 5, 100))
    session1.add_set(CardioSet(running, 30))


    # Antra treniruote
    session2 = WorkoutSession("2026-04-12")
    session2.add_set(StrengthSet(bench, 6, 90))
    session2.add_set(StrengthSet(squat, 5, 110))
    session2.add_set(CardioSet(running, 35))



    # STRENGTH TRACKER
    strength_tracker = ProgressTracker(StrengthProgressStrategy())
    strength_tracker.add_workout_session(session1)
    strength_tracker.add_workout_session(session2)

    print("=== STRENGTH PROGRESS ===")
    print("Bench Press progress:",
          strength_tracker.calculate_progress("Bench Press"))

    print("Squat progress:",
          strength_tracker.calculate_progress("Squat"))


    # CARDIO TRACKER
    cardio_tracker = ProgressTracker(CardioProgressStrategy())
    cardio_tracker.add_workout_session(session1)
    cardio_tracker.add_workout_session(session2)

    print("\n=== CARDIO PROGRESS ===")
    print("Running progress:",
          cardio_tracker.calculate_progress("Running"))