from __future__ import annotations

# defaultdict is used to count study sessions per day easily
from collections import defaultdict

# datetime is used to track time for streaks and plant state
from datetime import datetime, timedelta

# Iterable allows the function to accept any list-like collection of sessions
from typing import Iterable


# LEVELS defines the XP thresholds for each plant stage.
# Each tuple = (minimum XP required, level number, stage name)
# The list is ordered from highest XP to lowest so we can check top-down.
LEVELS = [
    (1000, 5, 'Full Bloom'),
    (500, 4, 'Growing Plant'),
    (250, 3, 'Young Seedling'),
    (100, 2, 'Cracking Sprout'),
    (0, 1, 'Tiny Seed'),
]


def calculate_level(xp: int) -> tuple[int, str]:
    """
    Determine the plant's level and stage based on total XP.

    The function loops through LEVELS and returns the first match
    where the user's XP meets the threshold.

    Returns:
        (level number, stage name)
    """
    for threshold, level, stage in LEVELS:
        if xp >= threshold:
            return level, stage

    # Fallback (should never happen due to 0 threshold)
    return 1, 'Tiny Seed'


def award_xp(
    event_type: str,
    *,
    minutes: int = 0,
    difficulty: int = 1,
    estimated_hours: float = 1.0
) -> int:
    """
    Calculate XP earned based on user actions.

    There are two types of events:
    1. 'session' → based on minutes studied
    2. 'assignment' → based on difficulty and estimated hours

    Rules:
    - Study sessions give XP proportional to time (with min and max limits)
    - Assignments give more XP depending on difficulty and size

    Returns:
        XP earned (integer)
    """

    # XP from a study session
    if event_type == 'session':
        # At least 10 XP, scaled by minutes studied
        base = max(10, minutes // 3)

        # Cap XP so very long sessions don’t give too much
        return min(base, 120)

    # XP from completing/adding an assignment
    if event_type == 'assignment':
        return 25 + (difficulty * 10) + int(estimated_hours * 5)

    # Unknown event type gives no XP
    return 0


def current_streak(sessions: Iterable) -> int:
    """
    Calculate the user's current study streak (in days).

    A streak is defined as:
    - consecutive days with at least one study session

    Steps:
    1. Count how many sessions happened on each date
    2. Start from today and move backwards
    3. Count how many consecutive days have activity

    Returns:
        number of consecutive active days
    """
    if not sessions:
        return 0

    # Count how many sessions occurred per day
    day_counts = defaultdict(int)
    for session in sessions:
        day_counts[session.completed_at.date()] += 1

    streak = 0
    current_day = datetime.utcnow().date()

    # Keep going backwards as long as the user studied each day
    while day_counts.get(current_day, 0) > 0:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


def calculate_plant_state(last_active_at: datetime, streak: int) -> str:
    """
    Determine the plant's mood/state.

    The plant's condition depends on:
    - how recently the user studied (inactivity)
    - whether the user is on a streak

    Rules:
    - 3+ day streak → Blooming (best state)
    - inactive > 3 days → Wilted (worst state)
    - inactive > 1 day → Droopy
    - otherwise → Happy

    Returns:
        string representing plant mood
    """
    now = datetime.utcnow()
    inactivity = now - last_active_at

    if streak >= 3:
        return 'Blooming'
    if inactivity > timedelta(days=3):
        return 'Wilted'
    if inactivity > timedelta(days=1):
        return 'Droopy'

    return 'Happy'
