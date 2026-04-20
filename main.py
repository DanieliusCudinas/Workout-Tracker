from tracker import ProgressTracker, BetweenSessionsStrategy, OverallStrategy
from workout import WorkoutSession, StrengthSet, CardioSet
from exercise import StrengthExercise, CardioExercise


def main():
    tracker = ProgressTracker(BetweenSessionsStrategy("weight"))

    while True:
        print("\n=== WORKOUT TRACKER ===")
        print("1. Add workout session")
        print("2. Show last sessions")
        print("3. Calculate progress")
        print("4. Save to file")
        print("5. Load from file")
        print("0. Exit")

        choice = input("Choose option: ")

        # EXIT
        if choice == "0":
            print("Goodbye!")
            break

        # ADD SESSION
        elif choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            session = WorkoutSession(date)

            while True:
                print("\nAdd set:")
                print("1. Strength")
                print("2. Cardio")
                print("0. Finish session")

                set_choice = input("Choose: ")

                if set_choice == "0":
                    break

                elif set_choice == "1":
                    try:
                        name = input("Exercise name: ")
                        muscle = input("Muscle: ")
                        reps = int(input("Reps: "))
                        weight = float(input("Weight: "))

                        ex = StrengthExercise(name, muscle)
                        s = StrengthSet(ex, reps, weight)
                        session.add_set(s)
                    except Exception as e:
                        print("Error:", e)

                elif set_choice == "2":
                    try:
                        name = input("Exercise name: ")
                        duration = float(input("Duration (min): "))

                        ex = CardioExercise(name)
                        s = CardioSet(ex, duration)
                        session.add_set(s)
                    except Exception as e:
                        print("Error:", e)

                else:
                    print("Invalid option")

            tracker.add_workout_session(session)
            print("Session added!")

        # SHOW LAST SESSIONS
        elif choice == "2":
            try:
                n = int(input("How many sessions to show: "))
                tracker.show_last_sessions(n)
            except:
                print("Invalid number")

        # CALCULATE PROGRESS
        elif choice == "3":
            name = input("Exercise name: ")

            print("Choose mode:")
            print("1. Between sessions")
            print("2. Overall")

            mode = input("Mode: ")

            print("Choose type:")
            print("1. Strength")
            print("2. Cardio")

            ex_type = input("Type: ")

            #metric ir strategy parenkami kartu
            if ex_type == "1":
                if mode == "1":
                    tracker.strategy = BetweenSessionsStrategy("weight")
                elif mode == "2":
                    tracker.strategy = OverallStrategy("weight")
                else:
                    print("Invalid mode")
                    continue

            elif ex_type == "2":
                if mode == "1":
                    tracker.strategy = BetweenSessionsStrategy("duration")
                elif mode == "2":
                    tracker.strategy = OverallStrategy("duration")
                else:
                    print("Invalid mode")
                    continue

            else:
                print("Invalid type")
                continue

            try:
                result = tracker.calculate_progress(name)

                if isinstance(result, dict):
                    print("\n=== Result ===")
                    print(f"Best result: {result["best"]}")
                    print(f"Last result: {result["last"]}")
                    print(f"Progress: {result["progress"]}")
                    print(f"Status: {result["status"]}")
                
                else:
                    print("Progress:", result)

            except Exception as e:
                print("Error:", e)

        # SAVE
        elif choice == "4":
            filename = input("Filename: ")
            tracker.save_to_file(filename)
            print("Saved!")

        # LOAD
        elif choice == "5":
            filename = input("Filename: ")
            tracker.load_from_file(filename)
            print("Loaded!")

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()