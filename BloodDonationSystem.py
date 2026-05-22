import mysql.connector
from mysql.connector import Error
from abc import ABC, abstractmethod


"""ABSTRACTION: The Searchable class is an abstract base class that defines the interface for searching by name and blood type. It abstracts away the details of how the search is implemented, allowing different classes to provide their own specific implementations while adhering to a common interface. This promotes a clear separation of concerns and allows for flexibility in how searching is performed across different classes."""

# Abstract class for the blood donation system

class Searchable(ABC):

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

    def __init__(self, name: str, age: int, contact: str, blood_type: str, weight: float):
        super().__init__(name, age, contact)
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

class BloodDonationDatabase(Searchable):

    """
    Will be using MariaDB to store and manage donor and recipient information. This class implements the Searchable interface, providing concrete implementations for searching by name and blood type.
    """

    def __init__(self, host, user, password, database):
        self.__config = {'host': host, 'user': user, 'password': password, 'database': database}

    def __get_connection(self):
        return mysql.connector.connect(**self.__config)
    
    def search_by_name(self, name: str):
        query = "SELECT name, age, contact, blood_type, weight FROM donors WHERE name = %s"

        try:
            connection = self.__get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (name,))
            row = cursor.fetchone()

            if row:
                return Donor(name=row[0], age=row[1], contact=row[2], blood_type=row[3], weight=row[4])
            
            return None # return None of there are no results or does not exist
        
        except Error as e:
            print(f"Error while connecting to database: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def search_by_blood_type(self, blood_type: str):
        """Queries the database and returns a list of Donor objects matching the blood type."""
        query = "SELECT name, age, contact, blood_type, weight FROM donors WHERE blood_type = %s"
        donor_list = [] # Initialize an empty list to hold our results

        try:
            connection = self.__get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (blood_type,))
            
            # 1. Fetch ALL rows that match (e.g., all 'O+' donors)
            rows = cursor.fetchall() 

            # 2. Loop through every row found
            for row in rows:
                # Create a Donor object for the current row
                matching_donor = Donor(
                    name=row[0], 
                    age=row[1], 
                    contact=row[2], 
                    blood_type=row[3], 
                    weight=row[4]
                )
                # Add this donor to our list
                donor_list.append(matching_donor)
            
            # 3. Return the populated list (will be empty [] if no matches found)
            return donor_list
        
        except Error as e:
            print(f"Error while connecting to database: {e}")
            return [] # Return an empty list if a database error happens
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()