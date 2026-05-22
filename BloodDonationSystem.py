from abc import ABC, abstractmethod 

# Abstract class for the blood donation system

class Searchable(ABC):

    """
    ABSTRACTION: The interface hides HOW searching works.
    Only the method names are exposed—implementation happens elsewhere.
    This defines a contract without specifying details.
    """

    @abstractmethod
    def search_by_name(self, name):
        """Search for a record by name"""
        pass

    @abstractmethod
    def search_by_blood_type(self, blood_type):
        """Search for a record by blood type"""
        pass

"""INHERITANCE: The Searchable class can be inherited by other classes (like Donor or Recipient) to implement specific search functionalities. This promotes code reuse and establishes a natural hierarchical relationship between classes."""

class Person:
    def __init__(self, name: str, age: int, contact: str):
        self.__name = name
        self.__age = age
        self.__contact = contact

        """ENCAPSULATION: The attributes are private (using __) and can only be accessed through methods. This hides the internal state and protects it from direct access, ensuring controlled interaction with the data."""

    def display_info(self):
        print(f"Name: {self.__name}")
        print(f"Age: {self.__age}")
        print(f"Contact: {self.__contact}")

    def get_name(self):
        return self.__name
    
    def get_age(self):
        return self.__age
    
    def get_contact(self):
        return self.__contact
    
class Donor(Person):

    """INHERITANCE: The Donor class inherits from the Person class, allowing it to reuse the attributes and methods of Person while adding its own specific attributes (blood type and weight) and behaviors (displaying donor-specific information)."""

    def __init__(self, name: str, age: int, blood_type: str, weight: float):
        super().__init__(name, age, contact="")
        self.__blood_type = blood_type
        self.__weight = weight

    def display_info(self):
        super().display_info()
        print(f"Blood Type: {self.__blood_type}")
        print(f"Weight: {self.__weight} kg")

    def get_blood_type(self):
        return self.__blood_type
    
    def get_weight(self):
        return self.__weight
    
    """POLYMORPHISM: The display_info method is overridden in the Donor class to provide specific details about donors. This allows the same method name to behave differently based on the context (i.e., whether it's called on a Person or a Donor), demonstrating polymorphism."""

    