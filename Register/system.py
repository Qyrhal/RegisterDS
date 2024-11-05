import employee
from typing import List
import csv
import constants
import numpy as np

class System:
    def __init__(self):
        self._employees: list = []

    def generate_employee_weighting(self) -> List[float]:
        """Generate a list of employee weightings"""
        employees = self._load_employees()
        return [employee.get_weighting() for employee in employees]

    def _load_employees(self) -> List[employee.Employee]:
        """Load employees from CSV file"""
        file_path = constants.Files.EMPLOYEES.value
        employees = []
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                min_hours = int(row['min_hours'])
                bar = row['bar'] == 'True'
                experience = float(row['experience'])
                opening = row['opening'] == 'True'
                closing = row['closing'] == 'True'
                # Collect availability in a list for all shifts in the week
                availability = [
                    row[shift] == 'Y' for shift in row.keys()
                    if "morning" in shift or "evening" in shift
                ]
                employees.append(
                    employee.Employee(name, min_hours, bar, experience,
                                   opening, closing, availability)
                )
        return employees

    def get_sorted_employees(self) -> List[employee.Employee]:
        """Get employees sorted by weighting"""
        return self.sorter(self._load_employees())

    @staticmethod
    def sorter(input_employees: List[employee.Employee]) -> np.ndarray:
        """
        Organize the employees based upon their weighting
        """
        return np.array(
            sorted(input_employees, 
                  key=lambda emp: emp.get_weighting(), 
                  reverse=True)
        )

    def calculate_shifts(self) -> np.ndarray:
        """Calculate weekly shift assignments"""
        employees = self.get_sorted_employees()
        # Create a new array of employees
        week_array = np.array([])
        
        for day in range(constants.Constants.DAYS_IN_WEEK.value):
            day_array = np.array([])
            
            for shift in range(constants.Constants.SHIFTS_PER_DAY.value):
                shift_array = np.array([])
                
                for employee in employees:
                    if employee.is_available(day, shift):  # You'll need to implement this method in Employee class
                        shift_array = np.append(shift_array, employee)
                        
                day_array = np.append(day_array, shift_array)
            week_array = np.append(week_array, day_array)
            
        return week_array


if __name__ == "__main__":
    # Create an instance of the System class
    system = System()
    # Now use the instance to call the method
    employees = system.calculate_shifts()
    print(employees)