# GrowPath CS32 Final Project 

## Features

**Plant Growth System**
- The plant grows when you complete assignments
- It wilts when you neglect your work and miss deadlines

**Assignment Tracking**
- Track assignments across multiple courses
- Set due dates and get visual status indicators
- Mark assignments as complete to grow your plant
- View assignment details and descriptions

**Customization**
- Give your plant a name 
- Customize its colors 
- Helps user become personally connected to the plant 

**Progress Tracking**
- Track completion rate
- See plant health status
- Monitor assignments over time

### Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd cs-32-final-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run growpath_python.py
```

The app will open in your default web browser at `http://localhost:8501`

## How It Works

### Plant Health System
- **Health Range**: 0-100%
- **Growth Stages**: Seed to Seedling to Sprout to Plant to Blooming
- **Health Gain**: 10-30 points per completed assignment (and scales with difficulty)
- **Health Decay**: Accelerating penalty for overdue assignments

### Assignment Status
- 🔴 **Overdue**: Past due date
- 🟠 **Due Today**: Due today
- 🟡 **Due Tomorrow**: Due tomorrow
- 🟢 **Upcoming**: Due in 2+ days
- ✅ **Completed**: Finished assignment

## Tech Stack
- **Streamlit**: Web app framework
- **Pandas**: Data manipulation
- **Python-dateutil**: Date parsing
- **Session State**: Data persistence (in-memory)

## Differences from FP Status Version
Our new version builds upon previous versions by preserving the original plant-based productivity system while making it more interactive and accessible. Earlier versions worked through the terminal, where users typed menu options to add assignments, log study sessions, view plant status, and generate plans. The new version expands this into a web app, allowing users to interact with the same core features through a visual dashboard. It also keeps the project organized by separating the plant growth logic from the user interface, making the app easier to maintain and improve in the future.

## Ways that AI was used 

1. Choosing Streamlit for instant UI

 helped  pick Streamlit as the framework, which:

turns Python into a web app with almost no frontend code
automatically renders UI in the browser
updates the interface in real time when state changes

2.Structuring the app (logic vs UI)

AI helped separate:

core logic (plant growth, health, assignment status)
UI layer (Streamlit components)

Examples:

get_plant_stage, calculate_health_gain → pure logic
Streamlit columns, buttons, forms → interface

3.Designing the plant growth system

 contributed to turning the idea into a working system with rules, like:

health range (0–100)
growth stages (Seed → Blooming)
decay formula for overdue work
reward scaling based on assignment difficulty

That’s not just coding—it’s system design.

4.Assignment tracking logic

overdue
due today
due tomorrow
upcoming
completed

And built functions like:

get_assignment_status
get_days_overdue

5. Generating test coverage

 test_growpath.py file is a big AI contribution:

validates plant stages
checks health calculations
verifies assignment logic

6. Session state management

AI guided the use of Streamlit session state, which:

stores assignments and plant health during runtime
allows the app to update interactively
avoids needing a database

7. UI/UX improvements



columns layout (plant vs assignments)
color-coded statuses (🔴 🟠 🟡 🟢 ✅)
progress bars
expanders and forms

8. Dependency & environment setup

requirements.txt for easy setup
clear run instructions (streamlit run ...)

9. Rapid prototyping

generated working code quickly
suggested improvements iteratively
helped debug issues (like running on other laptops)


## Future Enhancements
- Database integration for persistent storage
- User authentication
- Plant growth animations
- Email notifications for due assignments
- Data export/import functionality
