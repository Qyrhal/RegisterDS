class Employee:
    """
    Employee class representing staff members with various attributes and weightings
    """
    def __init__(self, name: str, min_hours: int, bar: bool, experience: bool, 
                 opening: bool, closing: bool, availability: list):
        self._name: str = name
        self._min_hours: int = min_hours
        self._bar: bool = bar
        self._experience: float = experience
        self._opening: bool = opening
        self._closing: bool = closing
        self._availability: list = availability
        self._weighting: float = self._calculate_weighting()


    def is_available(self, day: int, shift: int) -> bool:
        for i in range(len(self._availability)):
            if i == day * 2 + shift and self._availability[i]:
                return True
        return False
    
    # getters
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

    def get_weighting(self) -> float:
        return self._weighting

    def _calculate_weighting(self) -> float:
        """
        Calculate the weighting for an employee based on their attributes
        :return: Weighting for the employee
        
        Complexity:
        Best Case: O(1)
        Worst Case: O(1)
        """
        weighting = 0.0
        
        if self.get_bar():
            weighting += 1.0
        if self.get_opening():
            weighting += 0.5
        if self.get_min_hours() < 10:
            weighting += 0.5  # increase the weighting if the employee has less than 10 hours
        if self.get_opening():
            weighting += 0.5
        if self.get_closing():
            weighting += 0.5
        if self.get_opening() and self.get_closing():
            weighting += 1.0
        weighting += self.get_experience()
        
        # average weighting is 3.5
        return weighting

    def __lt__(self, other):
        """Compare employees based on their weighting"""
        return self.get_weighting() < other.get_weighting()

    def __str__(self):
        """Return a user-friendly string representation"""
        return f"Employee: {self.get_name()} (Weighting: {self.get_weighting():.2f})"

    def __repr__(self):
        # """Return a detailed string representation"""
        # return (f"Employee(name='{self._name}', min_hours={self._min_hours}, "
        #         f"bar={self._bar}, experience={self._experience}, "
        #         f"opening={self._opening}, closing={self._closing}, "
        #         f"availability={self._availability})")
        return f"Employee(name='{self._name}', weighting={self.get_weighting():.2f})"


if __name__ == "__main__":
    # Test cases
    billy = Employee("Billy", 20, True, True, True, True, [None])
    jane = Employee("Jane", 10, False, True, False, True, [None])
    
    print(billy)  # Will use __str__
    print(repr(billy))  # Will use __repr__
    print(f"Billy's weighting: {billy.get_weighting()}")
    print(f"Jane's weighting: {jane.get_weighting()}")