class Employee:
    """
    Employee class representing staff members with various attributes and weightings.
    
    Attributes:
        name (str): Employee's name
        min_hours (int): Minimum required hours per week
        bar (bool): Whether employee can work the bar
        experience (float): Years of experience
        opening (bool): Whether employee can work opening shifts
        closing (bool): Whether employee can work closing shifts
        availability (list): List of shift availability (True/False for each shift)
    """
    
    def __init__(self, name: str, min_hours: int, bar: bool, experience: float,
                 opening: bool, closing: bool, availability: list):
        self._name: str = name
        self._min_hours: int = min_hours
        self._bar: bool = bar
        self._experience: float = experience
        self._opening: bool = opening
        self._closing: bool = closing
        self._availability: list = availability
        self._worked_hours: int = 0
        self._weighting: float = self._calculate_weighting()

    def is_available(self, day: int, shift: int) -> bool:
        """
        Check if employee is available for a specific day and shift.
        
        Args:
            day (int): Day of the week (0-6)
            shift (int): Shift number (0-1 for morning/evening)
            
        Returns:
            bool: True if employee is available, False otherwise
        """
        index = day * 2 + shift
        return index < len(self._availability) and self._availability[index]

    def add_shift(self) -> None:
        """Add a shift to the employee's worked hours (typically 4 hours per shift)"""
        self._worked_hours += 4

    # Getters
    def get_name(self) -> str:
        return self._name

    def get_min_hours(self) -> int:
        return self._min_hours

    def get_bar(self) -> bool:
        return self._bar

    def get_availability(self) -> list:
        return self._availability

    def get_experience(self) -> float:
        return self._experience

    def get_opening(self) -> bool:
        return self._opening

    def get_closing(self) -> bool:
        return self._closing

    def get_worked_hours(self) -> int:
        return self._worked_hours

    def get_weighting(self) -> float:
        return self._weighting

    # Setters
    def set_hours(self, hours: int) -> None:
        """Set the number of hours worked"""
        self._worked_hours = hours

    def _calculate_weighting(self) -> float:
        """
        Calculate the weighting for an employee based on their attributes.
        
        The weighting is used to prioritize employees for shift assignments.
        Higher weights indicate more valuable employees for scheduling.
        
        Returns:
            float: Calculated weight value
            
        Complexity:
            Best Case: O(1)
            Worst Case: O(1)
        """
        weighting = 0.0
        
        # Base skills
        if self.get_bar():
            weighting += 1.0
        if self.get_opening():
            weighting += 0.5
        if self.get_closing():
            weighting += 0.5
            
        # Schedule flexibility
        if self.get_min_hours() < 10:
            weighting += 0.5  # Preference for part-time workers
        if self.get_opening() and self.get_closing():
            weighting += 1.0  # Bonus for full flexibility
            
        # Experience factor
        weighting += self.get_experience()
        
        return weighting

    def __lt__(self, other) -> bool:
        """
        Compare employees based on their weighting.
        
        Args:
            other (Employee): Another employee to compare with
            
        Returns:
            bool: True if this employee's weighting is less than the other's
        """
        return self.get_weighting() < other.get_weighting()

    def __str__(self) -> str:
        """Return a user-friendly string representation"""
        return (f"Employee: {self.get_name()} "
                f"(Weighting: {self.get_weighting():.2f}, "
                f"Hours: {self.get_worked_hours()}/{self.get_min_hours()})")

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging"""
        return (
            f"Employee(name='{self._name}', "
            f"min_hours={self._min_hours}, "
            f"bar={self._bar}, "
            f"experience={self._experience}, "
            f"opening={self._opening}, "
            f"closing={self._closing}, "
            f"availability={self._availability})"
        )


if __name__ == "__main__":
    # Test cases
    test_availability = [True] * 14  # 7 days * 2 shifts, all available
    
    employees = [
        Employee("Billy", 20, True, 3.5, True, True, test_availability),
        Employee("Jane", 10, False, 2.0, False, True, test_availability),
        Employee("Alex", 15, True, 1.5, True, False, test_availability),
    ]
    
    print("\nEmployee Details:")
    for emp in employees:
        print(f"\n{emp}")
        print(f"Can work bar: {emp.get_bar()}")
        print(f"Can open: {emp.get_opening()}")
        print(f"Can close: {emp.get_closing()}")
        print(f"Experience: {emp.get_experience()} years")
        print(f"Weighting: {emp.get_weighting():.2f}")
    
    # Test availability checking
    test_emp = employees[0]
    print(f"\nTesting availability for {test_emp.get_name()}:")
    print(f"Monday morning (0,0): {test_emp.is_available(0, 0)}")
    print(f"Wednesday evening (2,1): {test_emp.is_available(2, 1)}")
    
    # Test hour tracking
    print(f"\nTesting hour tracking for {test_emp.get_name()}:")
    print(f"Initial hours: {test_emp.get_worked_hours()}")
    test_emp.add_shift()
    print(f"After one shift: {test_emp.get_worked_hours()}")
    test_emp.add_shift()
    print(f"After two shifts: {test_emp.get_worked_hours()}")