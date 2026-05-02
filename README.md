# 🌱 GrowPath Python - Student Productivity & Plant Growth App

A Python implementation of GrowPath using Streamlit - a deeply personal, customizable plant-growth app that motivates students to complete assignments across an entire semester.

## Features

🌱 **Plant Growth System**
- Your plant grows as you complete assignments
- Wilts when you neglect your work and miss deadlines
- Reflects your productivity in real-time

📝 **Assignment Tracking**
- Track assignments across multiple courses
- Set due dates and get visual status indicators
- Mark assignments as complete to grow your plant
- View assignment details and descriptions

🎨 **Customization**
- Choose your plant's name
- Customize plant colors
- Create a plant that feels personally meaningful

📊 **Progress Tracking**
- Track completion rate
- See plant health status
- Monitor assignment timeline

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

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
- **Growth Stages**: Seed → Seedling → Sprout → Plant → Blooming
- **Health Gain**: 10-30 points per completed assignment (scales with difficulty)
- **Health Decay**: Accelerating penalty for overdue assignments

### Assignment Status
- 🔴 **Overdue**: Past due date
- 🟠 **Due Today**: Due today
- 🟡 **Due Tomorrow**: Due tomorrow
- 🟢 **Upcoming**: Due in 2+ days
- ✅ **Completed**: Finished assignments

## Tech Stack
- **Streamlit**: Web app framework
- **Pandas**: Data manipulation
- **Python-dateutil**: Date parsing
- **Session State**: Data persistence (in-memory)

## Differences from React Version
- **Pure Python**: No JavaScript required
- **Streamlit UI**: Different visual design but same functionality
- **Session-based**: Data persists during session (not localStorage)
- **Real-time Updates**: Automatic UI updates on state changes

## Future Enhancements
- Database integration for persistent storage
- User authentication
- Plant growth animations
- Email notifications for due assignments
- Data export/import functionality