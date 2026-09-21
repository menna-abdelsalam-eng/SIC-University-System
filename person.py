#Base class for: Student, Instructor and Admin
import re
class Person:
    def __init__(self, id, name, email, password,dept):
        #Validating User input
        while type(name) is not str or name == "":
            print("Invalid name")
            name = input("Enter name again: ")

        while not re.search(r'^(\w+)@(\w+)\.(\w+)$', email):
            print("Invalid email")
            email = input("Enter email again: ")

        while password == "" or len(password)<8:
            print("Invalid password")
            password = input("Enter password again: ")

        #Common Attributes across all the inherited classes
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.dept = dept

    def display_profile(self):
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Department: {self.dept}")
        print("_"*100)
    #Method is Overridden by the subclasses (polymorphism)
    def get_role(self):
        return "Person"