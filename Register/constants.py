from enum import Enum

class Constants(Enum):
    DAYS_IN_WEEK = 7
    SHIFTS_PER_DAY = 2  # Morning and Evening shifts
    MORNING_SHIFT = "10:45 am - 3:00 pm"
    EVENING_SHIFT = "4:45 pm - 9:00 pm"

class Days(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"