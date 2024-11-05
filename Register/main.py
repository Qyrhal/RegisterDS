import csv
from enum import Enum
from typing import List, Dict
import random
import employee

import constants


## DO NOT USE THIS CODE, AI GENERATED SHIT ASS

def generate_roster(employees: List[employee.Employee]) -> Dict[str, Dict[str, List[str]]]:
    roster = {day: {"Morning": [], "Evening": []} for day in constants.Days}
    shift_index = 0  # Track shifts across the week (0: Monday Morning, 1: Monday Evening, ..., 13: Sunday Evening)

    for day in roster.keys():
        for shift in roster[day].keys():
            available_employees = [e for e in employees if e.is_available(shift_index)]
            bar_trained = [e for e in available_employees if e.get_bar()]
            
            # Ensure at least one bar-trained employee
            if bar_trained:
                selected_employee = random.choice(bar_trained)
                roster[day][shift].append(selected_employee.get_name())
                selected_employee.assign_shift()
                available_employees.remove(selected_employee)
            
            # Fill remaining slots
            while len(roster[day][shift]) < 2 and available_employees:
                selected_employee = random.choice(available_employees)
                roster[day][shift].append(selected_employee.get_name())
                selected_employee.assign_shift()
                available_employees.remove(selected_employee)

            shift_index += 1

    return roster

if __name__ == "__main__":
    path = "Register/employees.txt"
    employees = load_employees(path)
    roster = generate_roster(employees)

    # Display the roster
    for day, shifts in roster.items():
        print(f"\n{day}:")
        for shift, assigned in shifts.items():
            print(f"  {shift} ({constants.Constants[shift].value}): {', '.join(assigned)}")