import datetime
from person import Person
class Secondary_Menu:
    def __init__(self,user,system):
        self.user = user
        self.system = system

    def view_menu(self):
        print("_" * 50, f"Welcome {self.user.name}", "_" * 50)


