from __future__ import annotations

# datetime is used to track when the user was last active
# and when study sessions were completed.
from datetime import datetime

# Import helper functions from plant_logic.py.
# These functions handle the core "game logic" of the project:
# - level calculation
# - XP rewards
# - streak calculation
# - plant mood/state
from plant_logic import (
    calculate_level,
    award_xp,
    current_streak,
    calculate_plant_state,
)

# Store assignments entered by the user.
# Each assignment is saved as a dictionary.
assignments = []

# Store all completed study sessions.
# Each session is saved as a StudySession object.
sessions = []

# Track the user's total XP across the program.
total_xp = 0

# Track the last time the user did something productive.
# This is used to determine whether the plant is Happy, Droopy, or Wilted.
last_active_at = datetime.utcnow()


class StudySession:
    """
    Represents one completed study session.

    Each session stores the time it was completed.
    This lets the program calculate a study streak based on dates.
    """
    def __init__(self, completed_at: datetime):
        self.completed_at = completed_at


def show_status() -> None:
    """
    Display the current plant status to the user.

    This function:
    1. Calculates the user's plant level and growth stage from total XP.
    2. Calculates the current streak from completed study sessions.
    3. Calculates the plant's mood based on inactivity and streak.
    4. Prints all of that information in a readable format.
    """
    level, stage = calculate_level(total_xp)
    streak = current_streak(sessions)
    mood = calculate_plant_state(last_active_at, streak)

    print("\n--- PLANT STATUS ---")
    print(f"XP: {total_xp}")
    print(f"Level: {level}")
    print(f"Stage: {stage}")
    print(f"Mood: {mood}")
    print(f"Streak: {streak} day(s)")


def add_assignment() -> None:
    """
    Let the user enter a new assignment.

    This function:
    1. Prompts for assignment information.
    2. Validates the numeric fields.
    3. Saves the assignment in the assignments list.
    4. Awards XP for adding an academic task.
    5. Updates the last active time so the plant stays healthy.
    """
    global total_xp, last_active_at

    print("\n--- ADD ASSIGNMENT ---")
    title = input("Assignment title: ").strip()
    due_date = input("Due date: ").strip()

    try:
        difficulty = int(input("Difficulty (1-5): ").strip())
        estimated_hours = float(input("Estimated hours: ").strip())
    except ValueError:
        print("Invalid number entered. Assignment not added.")
        return

    # Title and due date are required fields.
    if not title or not due_date:
        print("Title and due date are required.")
        return

    # Save assignment data in a dictionary.
    assignments.append(
        {
            "title": title,
            "due_date": due_date,
            "difficulty": difficulty,
            "estimated_hours": estimated_hours,
        }
    )

    # Award XP based on assignment difficulty and estimated hours.
    xp_earned = award_xp(
        "assignment",
        difficulty=difficulty,
        estimated_hours=estimated_hours,
    )
    total_xp += xp_earned

    # Update activity timestamp so plant state reflects engagement.
    last_active_at = datetime.utcnow()

    print(f"Assignment added. You earned {xp_earned} XP.")


def log_study_session() -> None:
    """
    Record a study session completed by the user.

    This function:
    1. Prompts the user for study duration in minutes.
    2. Validates that the value is a positive integer.
    3. Awards XP for the session.
    4. Updates the last active time.
    5. Stores the session so streaks can be calculated later.
    """
    global total_xp, last_active_at

    print("\n--- LOG STUDY SESSION ---")
    try:
        minutes = int(input("Minutes studied: ").strip())
    except ValueError:
        print("Please enter a valid whole number.")
        return

    if minutes <= 0:
        print("Minutes must be greater than 0.")
        return

    # Award XP based on the length of the study session.
    xp_earned = award_xp("session", minutes=minutes)
    total_xp += xp_earned

    # Update last active time to show the user has studied recently.
    last_active_at = datetime.utcnow()

    # Save the completed session for streak tracking.
    sessions.append(StudySession(datetime.utcnow()))

    print(f"Study session logged. You earned {xp_earned} XP.")


def show_assignments() -> None:
    """
    Print all assignments currently stored in the system.

    If there are no assignments yet, the user is informed.
    Otherwise, each assignment is printed with its details.
    """
    print("\n--- ASSIGNMENTS ---")
    if not assignments:
        print("No assignments added yet.")
        return

    for index, item in enumerate(assignments, start=1):
        print(
            f"{index}. {item['title']} | Due: {item['due_date']} | "
            f"Difficulty: {item['difficulty']} | "
            f"Estimated Hours: {item['estimated_hours']}"
        )


def generate_study_plan() -> None:
    """
    Generate a simple study plan from the assignments list.

    This is a rule-based planner:
    - assignments are sorted by due date
    - the user is reminded to study earlier tasks first

    For this class version, this is a lightweight alternative to a full AI planner.
    """
    print("\n--- STUDY PLAN ---")
    if not assignments:
        print("No assignments yet. Add one first.")
        return

    # Sort assignments by due date string.
    # Best results happen when dates are entered consistently,
    # for example: YYYY-MM-DD.
    sorted_assignments = sorted(assignments, key=lambda item: item["due_date"])

    for item in sorted_assignments:
        print(
            f"- Study for '{item['title']}' before {item['due_date']} "
            f"(difficulty {item['difficulty']}, "
            f"estimated {item['estimated_hours']} hrs)"
        )


def main() -> None:
    """
    Main program loop for the terminal application.

    This function continuously displays a menu and calls
    the correct feature based on the user's input.
    The loop ends only when the user selects Quit.
    """
    while True:
        print("\n====== GROWTH PATH ======")
        print("1. Show plant status")
        print("2. Add assignment")
        print("3. Log study session")
        print("4. View assignments")
        print("5. Generate study plan")
        print("6. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_status()
        elif choice == "2":
            add_assignment()
        elif choice == "3":
            log_study_session()
        elif choice == "4":
            show_assignments()
        elif choice == "5":
            generate_study_plan()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1-6.")


# This ensures the program runs only when the file is executed directly,
# not when it is imported into another Python file.
if __name__ == "__main__":
    main()
