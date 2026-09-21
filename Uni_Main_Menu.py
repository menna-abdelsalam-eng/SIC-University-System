from Authentication import Authentication
from Student_Secondary_Menu import Student_Secondary_Menu
from Instructor_Secondary_Menu import Instructor_Secondary_Menu
from Admin_Secondry_Menu import Admin_Secondary_Menu

class Main_Menu:
    def __init__(self,system):
        self.system=system
        self.authentication=Authentication(system)

    def display_menu(self):
        print("_" * 50, "Welcome to SIC University", "_" * 50)
        print(
            "1. Log in into your account\n"
            "2. Sign up\n"
            "3. Quit\n"
        )


    def run_menu(self):
        while True:
            self.display_menu()
            user_choice=input("Please enter your choice: ").strip()
            if user_choice == "1":
                user=self.authentication.login()
                if user is not None:
                    self.open_user_menu(user)
            elif user_choice == "2":
                user=self.authentication.register()
                if user is not None:
                    self.open_user_menu(user)
            elif user_choice == "3":
                print("Thank you for using SIC University System")
                break
            else:
                print("Invalid choice")

    # Open secondary menu based on the authenticated user's role
    def open_user_menu(self,user):
        role=user.get_role()

        if role=="Student":
            menu=Student_Secondary_Menu(user,self.system)

        elif role=="Instructor":
            menu=Instructor_Secondary_Menu(user,self.system)

        elif role=="Admin":
            menu=Admin_Secondary_Menu(user,self.system)

        else:
            print("Unknown user role.")
            return
        menu.view_menu()













