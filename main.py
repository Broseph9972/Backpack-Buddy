import LCD_1in44
import time
import json
import os
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageColor

# Load the schedule configuration
def load_schedule():
    try:
        with open('school_schedule.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: school_schedule.json not found. Please run schedule_config.py first.")
        return None

def parse_time(time_str):
    """Convert time string (HH:MM) to datetime object"""
    return datetime.strptime(time_str, "%H:%M").time()

def get_current_period(schedule):
    now = datetime.now().time()
    current_time = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
    
    # Parse schedule times
    start_time = datetime.strptime(schedule['school_start_time'], "%H:%M")
    end_time = datetime.strptime(schedule['school_end_time'], "%H:%M")
    
    # Check if school is in session
    if current_time < start_time:
        return "School hasn't started yet"
    if current_time > end_time:
        return "School is over"
    
    # Calculate time since school started
    time_elapsed = (current_time - start_time).total_seconds() / 60  # in minutes
    
    # Calculate period times
    current_minute = 0
    
    # Check if we're in homeroom
    if schedule['has_homeroom']:
        homeroom_end = schedule['homeroom_duration']
        if time_elapsed < homeroom_end:
            return schedule['homeroom_period_name']
        current_minute = homeroom_end + schedule['time_between_classes']
    
    # Check regular periods
    for period in schedule['periods']:
        period_end = current_minute + period['duration']
        if time_elapsed < period_end:
            return period['name']
        current_minute = period_end + schedule['time_between_classes']
    
    # Check if we're in a passing period
    return "Passing period"

def display_period(schedule):
    # Initialize LCD
    LCD = LCD_1in44.LCD()
    Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT
    LCD.LCD_Init(Lcd_ScanDir)
    
    # Create image with white background
    image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to load a font, fall back to default if not available
        font = ImageFont.load_default()
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            pass
            
        while True:
            # Clear the screen
            draw.rectangle([(0, 0), (LCD.width, LCD.height)], fill="WHITE")
            
            # Get current period
            period = get_current_period(schedule)
            
            # Draw period text in bottom right
            text_bbox = draw.textbbox((0, 0), period, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Position in bottom right with some padding
            x = LCD.width - text_width - 5
            y = LCD.height - text_height - 5
            
            # Draw background for better visibility
            draw.rectangle([x-2, y-2, x + text_width + 2, y + text_height + 2], fill="BLACK")
            
            # Draw the text
            draw.text((x, y), period, font=font, fill="WHITE")
            
            # Update the display
            LCD.LCD_ShowImage(image, 0, 0)
            
            # Wait a bit before updating again
            time.sleep(30)  # Update every 30 seconds
            
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Clear the display on exit
        LCD.LCD_Clear()
        LCD_1in44.TP_Shutdown()

def main():
    # Load the schedule
    schedule = load_schedule()
    if not schedule:
        return
    
    # Start displaying the current period
    display_period(schedule)

if __name__ == '__main__':
    main()