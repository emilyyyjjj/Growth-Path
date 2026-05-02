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


## Future Enhancements
- Database integration for persistent storage
- User authentication
- Plant growth animations
- Email notifications for due assignments
- Data export/import functionality
