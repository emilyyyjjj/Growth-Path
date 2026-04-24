from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Iterable


LEVELS = [
    (1000, 5, 'Full Bloom'),
    (500, 4, 'Growing Plant'),
    (250, 3, 'Young Seedling'),
    (100, 2, 'Cracking Sprout'),
    (0, 1, 'Tiny Seed'),
]


def calculate_level(xp: int) -> tuple[int, str]:
    for threshold, level, stage in LEVELS:
        if xp >= threshold:
            return level, stage
    return 1, 'Tiny Seed'


def award_xp(event_type: str, *, minutes: int = 0, difficulty: int = 1, estimated_hours: float = 1.0) -> int:
    if event_type == 'session':
        base = max(10, minutes // 3)
        return min(base, 120)
    if event_type == 'assignment':
        return 25 + (difficulty * 10) + int(estimated_hours * 5)
    return 0


def current_streak(sessions: Iterable) -> int:
    if not sessions:
        return 0

    day_counts = defaultdict(int)
    for session in sessions:
        day_counts[session.completed_at.date()] += 1

    streak = 0
    current_day = datetime.utcnow().date()

    while day_counts.get(current_day, 0) > 0:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


def calculate_plant_state(last_active_at: datetime, streak: int) -> str:
    now = datetime.utcnow()
    inactivity = now - last_active_at

    if streak >= 3:
        return 'Blooming'
    if inactivity > timedelta(days=3):
        return 'Wilted'
    if inactivity > timedelta(days=1):
        return 'Droopy'
    return 'Happy'
