# Workout Tracker

## What is the application?

This application is a workout progress tracking system built using Python and object-oriented programming (OOP) principles. It allows users to record workout sessions, manages exercises and tracks their progress over time.

---

## How to run the program?

### First way

1. Open the project folder in a terminal
2. Run the following command: py main.py (or python main.py depending on your system)

### Second way

1. Open file main.py
2. Run the program using VS Code

---

## How to use the program?

1. Open the application
2. Choose one of the options from the main menu:
    - Add workout session
    - Show last sessions
    - Calculate progress

3. Add workout session
    - Enter sessions date in YYYY-MM-DD format
    - Choose set type
    - Choose exercise from one of the options
    - When you filled essential information depending on your set type (muscle, reps, weight for strength set and duration for cardio set) press 'Add set' button to add set to the session
    - You can delete a set. To do so choose set on the list and then press 'Delete selected' button
    - You can edit a set. To do so choose set on the list and then press 'Edit selected' button. After that you can change information of your set
    - When you finish filling the session list press 'Save session' button to save your information

4. Show last sessions
    - You can see your last made sessions on that list with all information about every exercise
    - If there are no sessions saved, a message will be displayed

5. Calculate progress
    - Choose exercise name
    - Choose set type
    - Choose mode
    - Between sessions mode. This mode allows you to see your progress of the chosen exercise made during last 2 times when that exercise was in the session
    - Overall mode. This mode allows you to see your progress from your best result and last result.

---

## Analysis

### Object-Oriented Programming Principles

#### 1. Encapsulation

Encapsulation means hiding internal data and allowing access only through methods.

In this project, encapsulation is used in classes such as `WorkoutSession` and `ProgressTracker`.  
The internal data (like sets and sessions) is stored inside objects and accessed through methods such as:
- `add_set()`
- `add_workout_session()`
- `calculate_progress()`

This ensures controlled data modification and prevents direct access to internal structures.

---

#### 2. Inheritance

Inheritance allows creating new classes based on existing ones.

In this project:
- `StrengthSet` and `CardioSet` are specialized versions of a general set concept
- `StrengthExercise` and `CardioExercise` extend exercise behavior

This allows code reuse and cleaner structure by avoiding duplication.

---

#### 3. Polymorphism

Polymorphism allows different objects to be treated in the same way.

In this program:
- Both `StrengthSet` and `CardioSet` are used in the same list (`session.sets`)
- The method `get_info()` is called on all sets, regardless of their type

Example:

```python
for s in session.sets:
    print(s.get_info())
```

Each object responds differently depending on its type.

---

#### 4. Abstraction

Abstraction means hiding complex logic and exposing only necessary functionality.

This is implemented using the `ProgressStrategy` class:

```python
class ProgressStrategy:
    def calculate(self, sessions, exercise_name):
        raise NotImplementedError
```

Concrete strategies:
- `BetweenSessionsStrategy`
- `OverallStrategy`

The UI does not need to know how progress is calculated — it simply calls:

```python
tracker.calculate_progress(name)
```

---

### Design Pattern – Strategy Pattern

This project uses the Strategy design pattern.

The Strategy pattern allows selecting different algorithms at runtime.

In this program:
- `BetweenSessionsStrategy` compares last two sessions
- `OverallStrategy` compares best result with last session

The strategy is selected dynamically:

```python
tracker.strategy = BetweenSessionsStrategy(metric)
```

or

```python
tracker.strategy = OverallStrategy(metric)
```

This pattern was chosen because:
- It allows flexible switching between algorithms
- It keeps the code modular and extendable
- It avoids large conditional statements (if/else)

---

### Composition and Aggregation

The program uses composition and aggregation principles.

- **Composition**:
  - `WorkoutSession` contains multiple sets
  - Sets cannot exist without a session

- **Aggregation**:
  - `ProgressTracker` stores multiple sessions
  - Sessions can exist independently of the tracker

This structure reflects real-world relationships and improves code organization.

---

### File Handling (Reading and Writing)

The application uses file operations to store and load data.

- JSON file (`data.json`) is used to save workout sessions
- Text files (`.txt`) are used to store exercise lists and muscle list (used for strength only)

Saving data:

```python
tracker.save_to_file("data.json")
```

Loading data:

```python
tracker.load_from_file("data.json")
```

Exercise lists are loaded from text files:

```python
strength_exercises = load_exercises("strength_exercises.txt")
```

This allows:
- Persistent storage of user data
- Easy modification of exercises without changing code

---

## Results

The application successfully allows users to:
- Track workout sessions
- Manage exercises efficiently
- Analyze progress over time
- Store and load data reliably

The system works as expected and provides accurate results based on user input.

---

## Conclusions

The project demonstrates the use of:
- Object-Oriented Programming
- File handling (JSON, text files)
- GUI development using Tkinter
- Strategy design pattern for flexible progress calculation

The application is modular, easy to extend, and user-friendly.

---

## Possible improvements

The application can be extended in several ways:

- Add graphical progress charts
- Replace JSON with a database (e.g., SQLite)
- Add user authentication
- Improve UI design
