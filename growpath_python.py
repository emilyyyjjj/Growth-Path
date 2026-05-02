"""
GrowPath - Student Productivity & Plant Growth App
A Python implementation using Streamlit
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
from dateutil import parser
import time
import uuid

# Plant logic constants
PLANT_STAGES = {
    'seed': {'name': 'Seed', 'health_min': 0, 'health_max': 20, 'emoji': '🌱'},
    'seedling': {'name': 'Seedling', 'health_min': 20, 'health_max': 40, 'emoji': '🌿'},
    'sprout': {'name': 'Sprout', 'health_min': 40, 'health_max': 60, 'emoji': '🌱'},
    'plant': {'name': 'Plant', 'health_min': 60, 'health_max': 80, 'emoji': '🌾'},
    'blooming': {'name': 'Blooming', 'health_min': 80, 'health_max': 100, 'emoji': '🌸'},
}

def get_plant_stage(health):
    """Get the current plant stage based on health"""
    if health >= PLANT_STAGES['blooming']['health_min']:
        return PLANT_STAGES['blooming']
    elif health >= PLANT_STAGES['plant']['health_min']:
        return PLANT_STAGES['plant']
    elif health >= PLANT_STAGES['sprout']['health_min']:
        return PLANT_STAGES['sprout']
    elif health >= PLANT_STAGES['seedling']['health_min']:
        return PLANT_STAGES['seedling']
    else:
        return PLANT_STAGES['seed']

def get_plant_status(health):
    """Get plant status description"""
    if health >= 80:
        return 'thriving'
    elif health >= 60:
        return 'growing'
    elif health >= 40:
        return 'stable'
    elif health >= 20:
        return 'struggling'
    else:
        return 'wilting'

def calculate_health_decay(days_overdue):
    """Calculate health decay for overdue assignments"""
    return min(20, days_overdue * (2 + days_overdue))

def calculate_health_gain(assignment):
    """Calculate health gain for completing an assignment"""
    base_gain = 10
    estimated_hours = assignment.get('estimated_hours', 5)
    bonus = (estimated_hours // 10) * 15
    return base_gain + bonus

def get_assignment_status(assignment):
    """Get the status of an assignment"""
    if assignment.get('completed', False):
        return 'completed'

    due_date = parser.parse(assignment['due_date']).date()
    today = date.today()

    if due_date < today:
        return 'overdue'
    elif due_date == today:
        return 'due-today'
    elif (due_date - today).days == 1:
        return 'due-tomorrow'
    else:
        return 'upcoming'

def get_days_overdue(due_date_str):
    """Get number of days an assignment is overdue"""
    due_date = parser.parse(due_date_str).date()
    today = date.today()
    days = (today - due_date).days
    return max(0, days)

def load_data():
    """Load assignments and plant data from session state"""
    if 'assignments' not in st.session_state:
        st.session_state.assignments = []
    if 'plant_health' not in st.session_state:
        st.session_state.plant_health = 10
    if 'plant_customization' not in st.session_state:
        st.session_state.plant_customization = {
            'name': 'My Plant',
            'color': '#5aa088'
        }

def save_data():
    """Save data to session state (in a real app, this would save to a file/database)"""
    pass  # Data persists in session state

def main():
    st.set_page_config(
        page_title="🌱 GrowPath",
        page_icon="🌱",
        layout="wide"
    )

    # Load data
    load_data()

    # Title
    st.title("🌱 GrowPath")
    st.markdown("*Student Productivity & Plant Growth App*")

    # Create two columns
    col1, col2 = st.columns([1, 2])

    with col1:
        # Plant visualization
        st.subheader("Your Plant")

        plant_stage = get_plant_stage(st.session_state.plant_health)
        plant_status = get_plant_status(st.session_state.plant_health)

        # Plant display
        st.markdown(f"""
        <div style="
            text-align: center;
            font-size: 120px;
            margin: 20px 0;
            filter: {'grayscale(' + str(100 - st.session_state.plant_health) + '%)' if st.session_state.plant_health < 100 else 'none'};
        ">
            {plant_stage['emoji']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**{st.session_state.plant_customization['name']}**")
        st.markdown(f"**Stage:** {plant_stage['name']}")
        st.markdown(f"**Health:** {st.session_state.plant_health}% - *{plant_status}*")

        # Progress bar
        st.progress(st.session_state.plant_health / 100)

        # Settings
        with st.expander("⚙️ Settings"):
            plant_name = st.text_input("Plant Name",
                                     value=st.session_state.plant_customization['name'])
            plant_color = st.color_picker("Plant Color",
                                        value=st.session_state.plant_customization['color'])

            if st.button("Update Plant"):
                st.session_state.plant_customization['name'] = plant_name
                st.session_state.plant_customization['color'] = plant_color
                st.success("Plant updated!")

    with col2:
        # Assignments section
        st.subheader("📝 Assignments")

        # Add assignment form
        with st.expander("➕ Add New Assignment"):
            with st.form("add_assignment"):
                course = st.text_input("Course")
                title = st.text_input("Assignment Title")
                description = st.text_area("Description")
                due_date = st.date_input("Due Date", min_value=date.today())
                estimated_hours = st.number_input("Estimated Hours", min_value=1, value=5)

                submitted = st.form_submit_button("Add Assignment")
                if submitted and title and course:
                    new_assignment = {
                        'id': str(uuid.uuid4()),
                        'course': course,
                        'title': title,
                        'description': description,
                        'due_date': due_date.isoformat(),
                        'estimated_hours': estimated_hours,
                        'completed': False,
                        'created_at': datetime.now().isoformat()
                    }
                    st.session_state.assignments.append(new_assignment)
                    st.success("Assignment added!")
                    st.rerun()

        # Display assignments
        if st.session_state.assignments:
            # Calculate health decay from overdue assignments
            total_decay = 0
            overdue_count = 0
            for assignment in st.session_state.assignments:
                if not assignment.get('completed', False):
                    days_overdue = get_days_overdue(assignment['due_date'])
                    if days_overdue > 0:
                        total_decay += calculate_health_decay(days_overdue)
                        overdue_count += 1

            if overdue_count > 0:
                avg_decay = total_decay / len(st.session_state.assignments)
                if avg_decay > 0:
                    st.session_state.plant_health = max(0, st.session_state.plant_health - avg_decay * 0.01)  # Small decay per check

            # Group assignments by status
            completed = [a for a in st.session_state.assignments if a.get('completed', False)]
            overdue = [a for a in st.session_state.assignments if get_assignment_status(a) == 'overdue']
            due_today = [a for a in st.session_state.assignments if get_assignment_status(a) == 'due-today']
            due_tomorrow = [a for a in st.session_state.assignments if get_assignment_status(a) == 'due-tomorrow']
            upcoming = [a for a in st.session_state.assignments if get_assignment_status(a) == 'upcoming']

            # Display assignments by priority
            def display_assignments(assignments, title, color):
                if assignments:
                    st.markdown(f"### {title}")
                    for assignment in assignments:
                        with st.container():
                            col_a, col_b = st.columns([3, 1])

                            with col_a:
                                status = get_assignment_status(assignment)
                                status_colors = {
                                    'overdue': '🔴',
                                    'due-today': '🟠',
                                    'due-tomorrow': '🟡',
                                    'upcoming': '🟢',
                                    'completed': '✅'
                                }

                                st.markdown(f"{status_colors.get(status, '📝')} **{assignment['title']}**")
                                st.caption(f"Course: {assignment['course']} | Due: {assignment['due_date']}")
                                if assignment.get('description'):
                                    st.caption(assignment['description'])

                            with col_b:
                                if not assignment.get('completed', False):
                                    if st.button("Complete", key=f"complete_{assignment['id']}"):
                                        # Calculate health gain
                                        health_gain = calculate_health_gain(assignment)
                                        st.session_state.plant_health = min(100, st.session_state.plant_health + health_gain)

                                        # Mark as completed
                                        for i, a in enumerate(st.session_state.assignments):
                                            if a['id'] == assignment['id']:
                                                st.session_state.assignments[i]['completed'] = True
                                                break

                                        st.success(f"Assignment completed! Plant gained {health_gain} health points!")
                                        st.rerun()
                                else:
                                    st.button("✅ Completed", disabled=True, key=f"completed_{assignment['id']}")

            display_assignments(overdue, "🔴 Overdue", "red")
            display_assignments(due_today, "🟠 Due Today", "orange")
            display_assignments(due_tomorrow, "🟡 Due Tomorrow", "yellow")
            display_assignments(upcoming, "🟢 Upcoming", "green")
            display_assignments(completed, "✅ Completed", "gray")

        else:
            st.info("No assignments yet. Add your first assignment to start growing your plant!")

        # Statistics
        total_assignments = len(st.session_state.assignments)
        completed_count = len([a for a in st.session_state.assignments if a.get('completed', False)])

        if total_assignments > 0:
            completion_rate = (completed_count / total_assignments) * 100
            st.markdown("---")
            st.markdown("### 📊 Progress")
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
            st.metric("Total Assignments", total_assignments)
            st.metric("Completed", completed_count)

if __name__ == "__main__":
    main()
