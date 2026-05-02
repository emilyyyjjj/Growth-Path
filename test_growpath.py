#!/usr/bin/env python3
"""
Test script for GrowPath Python functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from growpath_python import (
    get_plant_stage,
    get_plant_status,
    calculate_health_decay,
    calculate_health_gain,
    get_assignment_status,
    get_days_overdue
)
from datetime import date, timedelta
import json

def test_plant_logic():
    """Test plant growth and health logic"""
    print("Testing Plant Logic...")

    # Test plant stages
    assert get_plant_stage(0)['name'] == 'Seed'
    assert get_plant_stage(25)['name'] == 'Seedling'
    assert get_plant_stage(50)['name'] == 'Sprout'
    assert get_plant_stage(75)['name'] == 'Plant'
    assert get_plant_stage(90)['name'] == 'Blooming'
    print("✓ Plant stages working correctly")

    # Test plant status
    assert get_plant_status(90) == 'thriving'
    assert get_plant_status(70) == 'growing'
    assert get_plant_status(50) == 'stable'
    assert get_plant_status(30) == 'struggling'
    assert get_plant_status(10) == 'wilting'
    print("✓ Plant status working correctly")

    # Test health calculations
    assert calculate_health_decay(1) == 3  # 1 * (2 + 1)
    assert calculate_health_decay(5) == 20  # min(20, 5 * (2 + 5))
    print("✓ Health decay calculation working correctly")

    # Test health gain
    assignment_easy = {'estimated_hours': 2}
    assignment_hard = {'estimated_hours': 15}
    assert calculate_health_gain(assignment_easy) == 10  # base 10, no bonus
    assert calculate_health_gain(assignment_hard) == 25  # base 10 + bonus 15
    print("✓ Health gain calculation working correctly")

def test_assignment_logic():
    """Test assignment status and date logic"""
    print("\nTesting Assignment Logic...")

    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=2)

    # Test assignment statuses
    completed_assignment = {'completed': True, 'due_date': today.isoformat()}
    overdue_assignment = {'completed': False, 'due_date': yesterday.isoformat()}
    due_today_assignment = {'completed': False, 'due_date': today.isoformat()}
    due_tomorrow_assignment = {'completed': False, 'due_date': (today + timedelta(days=1)).isoformat()}
    upcoming_assignment = {'completed': False, 'due_date': tomorrow.isoformat()}

    assert get_assignment_status(completed_assignment) == 'completed'
    assert get_assignment_status(overdue_assignment) == 'overdue'
    assert get_assignment_status(due_today_assignment) == 'due-today'
    assert get_assignment_status(due_tomorrow_assignment) == 'due-tomorrow'
    assert get_assignment_status(upcoming_assignment) == 'upcoming'
    print("✓ Assignment status working correctly")

    # Test days overdue
    assert get_days_overdue(yesterday.isoformat()) == 1
    assert get_days_overdue((today - timedelta(days=3)).isoformat()) == 3
    assert get_days_overdue(tomorrow.isoformat()) == 0  # Not overdue
    print("✓ Days overdue calculation working correctly")

def main():
    """Run all tests"""
    print("🧪 Testing GrowPath Python Implementation")
    print("=" * 50)

    try:
        test_plant_logic()
        test_assignment_logic()

        print("\n" + "=" * 50)
        print("✅ All tests passed! GrowPath Python is working correctly.")
        print("\n🚀 You can now run: streamlit run growpath_python.py")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()