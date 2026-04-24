from __future__ import annotations

from datetime import datetime
from plant_logic import (
    calculate_level,
    award_xp,
    current_streak,
    calculate_plant_state,
)


assignments = []
sessions = []
total_xp = 0
last_active_at = datetime.utcnow()


class StudySession:
    def __init__(self, completed_at: datetime):
        self.completed_at = completed_at


def show_status() -> None:
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

    if not title or not due_date:
        print("Title and due date are required.")
        return

    assignments.append(
        {
            "title": title,
            "due_date": due_date,
            "difficulty": difficulty,
            "estimated_hours": estimated_hours,
        }
    )

    xp_earned = award_xp(
        "assignment",
        difficulty=difficulty,
        estimated_hours=estimated_hours,
    )
    total_xp += xp_earned
    last_active_at = datetime.utcnow()

    print(f"Assignment added. You earned {xp_earned} XP.")


def log_study_session() -> None:
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

    xp_earned = award_xp("session", minutes=minutes)
    total_xp += xp_earned
    last_active_at = datetime.utcnow()

    sessions.append(StudySession(datetime.utcnow()))

    print(f"Study session logged. You earned {xp_earned} XP.")


def show_assignments() -> None:
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
    print("\n--- STUDY PLAN ---")
    if not assignments:
        print("No assignments yet. Add one first.")
        return

    sorted_assignments = sorted(assignments, key=lambda item: item["due_date"])

    for item in sorted_assignments:
        print(
            f"- Study for '{item['title']}' before {item['due_date']} "
            f"(difficulty {item['difficulty']}, "
            f"estimated {item['estimated_hours']} hrs)"
        )


def main() -> None:
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


if __name__ == "__main__":
    main()
