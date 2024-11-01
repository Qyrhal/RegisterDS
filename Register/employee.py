
class Employee:
    """
    Employee class
    """

    def __init__(self, name: str, min_hours: int, bar: bool, availability: list):
        self._name: str = name
        self._min_hours: int = min_hours
        self._bar: bool = bar
        self._availability: list = availability

    # getters

    def get_name(self) -> str:
        return self._name
    
    def get_min_hours(self) -> int:
        return self._min_hours
    
    def get_bar(self) -> bool:
        return self._bar
    
    def get_availability(self) -> list:
        return self._availability
    

