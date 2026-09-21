#Represents Instructor specific menu
from Uni_Secondary_Menu import Secondary_Menu
from instructor import *
from Instructor_Report import *
from Instructor_Dashboard import Instructor_Dashboard

class Instructor_Secondary_Menu(Secondary_Menu):
    def __init__(self,instructor,system):
        super().__init__(instructor,system)
        self.instructor = instructor
        self.system = system

    def view_menu(self):
        while True:
            print("_"*50,f"Welcome Dr.{self.instructor.name}","_"*50)
            print(
                " 1. Add Course\n"
                " 2. Remove My Course\n"
                " 3. View My Courses\n"
                " 4. View My Enrolled Students\n"
                " 5. Add Student to My Roster\n"
                " 6. Enroll Students in Course\n"
                " 7. Drop Student from Course\n"
                " 8. Add Grade to Student\n"
                " 9. Display Reports\n"
                "10. View my Dashboard\n"
                "11. Back to Main Menu\n "
            )
            choice = input("Please enter your choice:\n")
            if choice == "11":
                print("Back to Main Menu")
                break
            self.set_instructor_choice(choice)

    def set_instructor_choice(self,choice):
        if choice == "1":
            self.system.add_course(self.instructor)
        elif choice == "2":
            self.system.remove_course(self.instructor)
        elif choice == "3":
            self.instructor.display_courses()
        elif choice == "4":
            print("_" * 50, "Students Data Base", "_" * 50)
            self.instructor.display_students()
        elif choice == "5":
            self.system.add_student_to_instructor_roster(self.instructor)
        elif choice == "6":
            self.system.instructor_enroll_student(self.instructor)
        elif choice == "7":
            self.system.instructor_drop_student(self.instructor)
        elif choice == "8":
            self.system.instructor_add_grade(self.instructor)
        elif choice == "9":
            report = Instructor_Report(self.instructor,self.system)
            report.display_menu()
        elif choice == "10":
            dashboard = Instructor_Dashboard(self.instructor, self.system)
            dashboard.dashboard_menu()
        else:
            print("Invalid Choice")






