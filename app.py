from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

from plant_logic import (
    calculate_level,
    award_xp,
    calculate_plant_state,
)

app = Flask(__name__)

# Simple class-project storage
assignments = []
sessions = []
total_xp = 0
last_active_at = datetime.utcnow()


class StudySession:
    def __init__(self, completed_at):
        self.completed_at = completed_at


@app.route("/")
def home():
    level, stage = calculate_level(total_xp)

    streak = 0
    if sessions:
        # optional: use your current_streak function later
        streak = len(sessions)

    plant_mood = calculate_plant_state(last_active_at, streak)

    plant = {
        "level": level,
        "stage": stage,
        "mood": plant_mood
    }

    return render_template(
        "dashboard.html",
        assignments=assignments,
        xp=total_xp,
        plant=plant
    )


@app.route("/add_assignment", methods=["POST"])
def add_assignment():
    global total_xp, last_active_at

    title = request.form.get("title")
    due_date = request.form.get("due_date")
    difficulty = int(request.form.get("difficulty", 1))
    estimated_hours = float(request.form.get("estimated_hours", 1))

    if title and due_date:
        assignments.append({
            "title": title,
            "due_date": due_date,
            "difficulty": difficulty,
            "estimated_hours": estimated_hours
        })

        xp_earned = award_xp(
            "assignment",
            difficulty=difficulty,
            estimated_hours=estimated_hours
        )
        total_xp += xp_earned
        last_active_at = datetime.utcnow()

    return redirect(url_for("home"))


@app.route("/complete_session", methods=["POST"])
def complete_session():
    global total_xp, last_active_at

    minutes = int(request.form.get("minutes", 0))

    xp_earned = award_xp("session", minutes=minutes)
    total_xp += xp_earned
    last_active_at = datetime.utcnow()

    sessions.append(StudySession(datetime.utcnow()))

    return redirect(url_for("home"))


@app.route("/study_plan")
def study_plan():
    plan = []

    if not assignments:
        plan.append("No assignments yet. Add one first.")
    else:
        for item in assignments:
            plan.append(
                f"Study for {item['title']} before {item['due_date']} "
                f"(difficulty {item['difficulty']}, est. {item['estimated_hours']} hrs)"
            )

    return render_template("plan.html", plan=plan)


if __name__ == "__main__":
    app.run(debug=True)
