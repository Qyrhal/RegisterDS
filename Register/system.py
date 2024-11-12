# cleaned up the code using AI, coz im a beta male

import employee
from typing import List, Optional
import csv
from csv import DictReader
import constants
import numpy as np
from dataclasses import dataclass
from typing import Dict, Set, Tuple
import os
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass # no need for constants class anymore, delete it future midhun
class ShiftRequirements:
    """Requirements for each shift"""
    min_employees: int = 5
    needs_bartender: bool = True
    needs_opener: bool = True
    needs_closer: bool = True

    def get_min_employees(self, day: int, shift: int):
        """
        Allows for overriding the default min_employees for specific days/shifts
        """
        # if day == 5 and shift == 1:  # Saturday Evening (day 5, shift 1)
        #     return 8
        # if day == 6 and shift == 0:  # Sunday Morning (day 6, shift 0)
        #     return 8
        return self.min_employees  # Default for other shifts


# made these coz im too good of a coder
class EmployeeSchedulerError(Exception):
    """Base exception for employee scheduler errors"""
    pass

class FileNotFoundError(EmployeeSchedulerError):
    """Raised when employee data file cannot be found"""
    pass

class EmployeeScheduler:
    """Handles employee shift scheduling and validation"""
    
    def __init__(self, file_path: str = None):
        if file_path:
            self.file_path = file_path
        else:
            # Try different possible file locations, coz this shit is fuckijgn me in the ass
            possible_paths = [
                constants.Files.EMPLOYEES.value,
                os.path.join('Register', 'employees.txt'),
                os.path.join('..', 'Register', 'employees.txt'),
                'employees.txt'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.file_path = path
                    break
            else:
                # If no file is found, raise an error with helpful message
                raise FileNotFoundError(
                    f"Could not find employee data file. Tried paths: {', '.join(possible_paths)}\n"
                    f"Current working directory: {os.getcwd()}\n"
                    "Please ensure the employee data file exists in one of these locations."
                )
                
        self.employees: List[employee.Employee] = []
        self.schedule: Dict[int, Dict[int, List[employee.Employee]]] = {}
        logger.info(f"Initialized EmployeeScheduler with file path: {self.file_path}")
        
    def load_employees(self) -> None:
        """Load employees from CSV file"""
        try:
            with open(self.file_path, 'r') as file:
                reader: DictReader = csv.DictReader(file)
                self.employees = [self._create_employee(row) for row in reader]
            logger.info(f"Successfully loaded {len(self.employees)} employees")
        except FileNotFoundError as e:
            logger.error(f"Employee data file not found: {self.file_path}")
            raise FileNotFoundError(f"Could not find employee data file at {self.file_path}")
        except csv.Error as e:
            logger.error(f"Error reading CSV file: {e}")
            raise EmployeeSchedulerError(f"Error reading employee data: {e}")
    
    @staticmethod
    def _create_employee(row: Dict[str, str]) -> employee.Employee:
        """Create an employee instance from a CSV row"""
        try:
            availability = [
                row[shift] == 'Y' for shift in row.keys()
                if "morning" in shift or "evening" in shift
            ]
            return employee.Employee(
                name=row['name'],
                min_hours=int(row['min_hours']),
                bar=row['bar'] == 'True',
                experience=float(row['experience']),
                opening=row['opening'] == 'True',
                closing=row['closing'] == 'True',
                availability=availability
            )
        except (KeyError, ValueError) as e:
            logger.error(f"Error creating employee from row: {row}")
            raise EmployeeSchedulerError(f"Invalid employee data format: {e}")

    def sort_employees(self) -> None:
        """Sort employees by weighting using merge sort"""
        self.employees = self._merge_sort(self.employees)

    def _merge_sort(self, employees: List[employee.Employee]) -> List[employee.Employee]:
        """Merge sort implementation for employee list"""
        if len(employees) <= 1:
            return employees
            
        mid = len(employees) // 2
        left = self._merge_sort(employees[:mid])
        right = self._merge_sort(employees[mid:])
        
        return self._merge_auxillary(left, right)
    
    def _merge_auxillary(self, left: List[employee.Employee], right: List[employee.Employee]) -> List[employee.Employee]:
        """Merge two sorted lists of employees"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i].get_weighting() > right[j].get_weighting():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def calculate_shifts(self) -> Dict[int, Dict[int, List[employee.Employee]]]:
        """
        Calculate weekly shift assignments
        
        Returns:
            Dict mapping days to shifts to list of assigned employees
        """
        try:
            self.load_employees()
            self.sort_employees()

            self.shift_requirements = ShiftRequirements() #initialize ShiftRequirements

            for day in range(7):
                self.schedule[day] = {}
                for shift in range(2):
                    assigned_employees = self._assign_shift(day, shift)
                    if assigned_employees:
                        self.schedule[day][shift] = assigned_employees
                        self._update_worked_hours(assigned_employees)
            
            logger.info("Successfully calculated shifts for the week")
            return self.schedule
            
        except Exception as e:
            logger.error(f"Error calculating shifts: {e}")
            raise EmployeeSchedulerError(f"Failed to calculate shifts: {e}")

    def _assign_shift(self, day: int, shift: int) -> Optional[List[employee.Employee]]:
        """
        Assign employees to a specific shift
        
        Args:
            day: Day of the week (0-6)
            shift: Shift number (0-1)
            
        Returns:
            List of assigned employees or None if requirements can't be met
        """
        available_employees = [
            emp for emp in self.employees
            if emp.is_available(day, shift) and 
            emp.get_worked_hours() < emp.get_min_hours()
        ]


        min_employees_for_shift = self.shift_requirements.get_min_employees(day, shift) # Get the minimum number of employees for this specific shift

        if not self._validate_shift_requirements(available_employees, shift, min_employees_for_shift): # Check requirements using new parameter
            logger.warning(f"Could not meet requirements for day {day}, shift {shift}")
            return None
            
        # Prioritize employees who need more hours to meet their minimum
        available_employees.sort(
            key=lambda x: (
                x.get_min_hours() - x.get_worked_hours(),
                x.get_weighting()
            ),
            reverse=True
        )
        
        return available_employees[:min_employees_for_shift] # Assign up to the specified minimum

    def _validate_shift_requirements(self, employees: List[employee.Employee], shift: int, min_employees_for_shift:int) -> bool: 
        """Validate that shift requirements can be met with available employees"""
        if len(employees) < min_employees_for_shift: # Modification: Use day/shift specific minimum
            return False
            
        # Morning shift needs opener and bartender
        if shift == 0 and ShiftRequirements.needs_opener:
            has_opener = any(emp.get_opening() for emp in employees)
            has_bartender = any(emp.get_bar() for emp in employees)
            if not (has_opener and has_bartender):
                return False

        # Evening shift needs closer
        if shift == 1 and ShiftRequirements.needs_closer:
            if not any(emp.get_closing() for emp in employees):
                return False
                
        return True

    @staticmethod
    def _update_worked_hours(employees: List[employee.Employee]) -> None:
        """Update worked hours for assigned employees"""
        for emp in employees:
            emp.add_shift()

def main():
    try:
        scheduler = EmployeeScheduler()
        schedule = scheduler.calculate_shifts()
        
        # Print schedule
        for day in range(7):
            print(f"\nDay {day}:")
            for shift in range(2):
                print(f"  Shift {shift}:")
                if day in schedule and shift in schedule[day]:
                    for emp in schedule[day][shift]:
                        print(f"    - {emp.get_name()}")
                else:
                    print("    No valid assignments found")
                    
    except EmployeeSchedulerError as e:
        logger.error(f"Scheduler error: {e}")
        print(f"Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()