#Represents student specific menu
from Uni_Secondary_Menu import Secondary_Menu

class Student_Secondary_Menu(Secondary_Menu):
    def __init__(self,student,system):
        super().__init__(student,system)
        self.student = student
        self.system = system

    def view_menu(self):
        while True:
            print("_"*50,f"Welcome {self.student.name} ","_"*50)
            print(
                "1. View My Schedule\n"
                "2. View Available Courses\n"
                "3. Enroll in a Course\n"
                "4. Drop a Course\n"
                "5. View My Courses\n"
                "6. View GPA Report\n"
                "7. Back to Main Menu\n"
            )
            choice = input("Please enter your choice:\n")
            if choice == "7":
                print("Back to Main Menu")
                break
            self.set_student_choice(choice)


    def time_table(self,courses):
        days = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu"]
        periods = range(1, 7)
        print("\n" + "_" * 160)
        print("_" * 60, "STUDENT SCHEDULE", "_" * 75)
        print("_" * 160)
        print(f"{'Period':20}", end="")
        for day in days:
            print(f"{day:25}", end="")
        print()
        print("-" * 160)
        for period in periods:
            print(f"{period:<10}", end="")
            for day in days:
                course_name = ""
                for course, (course_day, course_period) in courses.items():
                    if course_day == day and course_period == period:
                        course_name = course
                print(f"| {course_name:20} |", end="")
            print()
        print("_" * 160)

    def set_student_choice(self,choice):
        if choice == "1":
            self.system.show_schedule(self.student)
        elif choice == "2":
            self.system.show_available_courses()
        elif choice == "3":
            self.system.student_enroll(self.student)
        elif choice == "4":
            self.system.student_drop(self.student)
        elif choice == "5":
            print("Here are your current courses:")
            self.student.display_courses()
        elif choice == "6":
            calculated_gpa = self.student.calculate_gpa()
            print("Your GPA is: ", calculated_gpa)


        else:
            print("Invalid Choice")


