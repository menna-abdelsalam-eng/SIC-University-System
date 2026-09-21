#Represents admin specific menu
from Uni_Secondary_Menu import Secondary_Menu

class Admin_Secondary_Menu(Secondary_Menu):
    def __init__(self,admin,system):
        super().__init__(admin,system)
        self.admin = admin
        self.system = system

    def view_menu(self):
        while True:
            print("_"*50,"Admin Menu","_"*50)
            print("1. View All Students\n"
                  "2. View All Instructors\n"
                  "3. View All Courses\n"
                  "4. View System Statistics\n"
                  "5. Add Course\n"
                  "6. Remove Course\n"
                  "7. Back to Main Menu\n")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.system.display_all_students()
            elif choice == "2":
                self.system.display_all_instructors()
            elif choice == "3":
                self.system.display_all_courses()
            elif choice == "4":
                self.system.display_system_statistics()
            elif choice == "5":
                self.system.admin_add_course()
            elif choice == "6":
                self.system.admin_remove_course()
            elif choice == "7":
                print("Back to Main Menu")
                break
            else:
                print("Invalid Choice")

