import json
import os
from datetime import datetime, time as dtime, timedelta

def get_time_input(prompt, default=None):
    while True:
        time_str = input(f"{prompt} (HH:MM)" + (f" [{default}]: " if default else ": "))
        if not time_str and default:
            return default
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            return time_obj.strftime("%H:%M")
        except ValueError:
            print("Please enter time in HH:MM format (e.g., 08:30)")

def get_int_input(prompt, min_val=1, max_val=20, default=None):
    while True:
        try:
            value = input(f"{prompt}" + (f" [{default}]: " if default is not None else ": "))
            if not value and default is not None:
                return default
            value = int(value)
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("Please enter a valid number")

def get_yes_no(prompt, default=None):
    while True:
        response = input(f"{prompt} (y/n)" + (f" [{'Y' if default else 'n'}]: " if default is not None else ": ")).lower()
        if not response and default is not None:
            return default
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")

def create_schedule_config():
    print("\n=== School Schedule Configuration ===\n")
    
    # School day configuration
    config = {
        'school_name': input("Enter school name: "),
        'school_start_time': get_time_input("School start time", "08:00"),
        'school_end_time': get_time_input("School end time", "15:00"),
        'has_homeroom': get_yes_no("Do you have homeroom?"),
        'days_per_cycle': get_int_input("Number of days in your school cycle: ", 1, 10, 5),
        'class_duration': get_int_input("Duration of each class (minutes): ", 10, 120, 45),
        'time_between_classes': get_int_input("Time between classes (minutes): ", 0, 30, 5),
    }
    
    # Homeroom details if applicable
    if config['has_homeroom']:
        config['homeroom_duration'] = get_int_input("Homeroom duration (minutes): ", 1, 120, 15)
        config['homeroom_period_name'] = input("Homeroom period name [Homeroom]: ") or "Homeroom"
    
    # Lunch configuration
    has_lunch = get_yes_no("Do you have lunch period?")
    if has_lunch:
        config['lunch'] = {
            'start_time': get_time_input("Lunch start time", "12:00"),
            'duration': get_int_input("Lunch duration (minutes): ", 10, 120, 30)
        }
    
    # Class periods
    print("\n=== Class Periods ===")
    num_periods = get_int_input("Number of class periods in a day: ", 1, 15, 8)
    config['periods'] = []
    
    # Get all period names first
    period_names = []
    for i in range(1, num_periods + 1):
        name = input(f"Name for Period {i} [Period {i}]: ") or f"Period {i}"
        period_names.append(name)
    
    # Create period configurations with uniform duration
    for i in range(1, num_periods + 1):
        period = {
            'number': i,
            'name': period_names[i-1],
            'duration': config['class_duration']
        }
        
        # If this is the first period, ask if it's before or after homeroom
        if i == 1 and config['has_homeroom']:
            period['before_homeroom'] = get_yes_no("  Is this period before homeroom?", False)
        
        config['periods'].append(period)
    
    # Save to file
    filename = 'school_schedule.json'
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"\nConfiguration saved to {os.path.abspath(filename)}")
    print("You can now use this configuration with your school clock program.")

if __name__ == "__main__":
    create_schedule_config()
