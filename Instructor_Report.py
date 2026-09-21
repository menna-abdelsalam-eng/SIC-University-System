from instructor import *
from course import *
class Instructor_Report:
    def __init__(self, instructor, system):
        self.instructor = instructor
        self.system = system

    def display_menu(self):
        print("_" * 50, "SIC Students\' Report", "_" * 50)
        while True:
            print("1. Enrollment Reports\n"
                  "2. Avaliable Seats\n"
                  "3. Students Insights\n"
                  "4. Back to Secondary Menu\n"
                  )
            report_choice = input("Please enter your choice:")
            if report_choice == "4":
                print("Returning to Secondary Menu")
                print()
                break
            self.instructor_report_choice(report_choice)

    # find the top 3 from each dept, Analyze students data
    def students_insights(self):
        departments = set(student.dept for student in self.system.students)
        print("____Students Insights___".center(50))
        for dept in departments:
            dept_students=list(filter(lambda student: student.dept == dept,self.system.students))
            dept_students=sorted(dept_students,key=lambda student:student.calculate_gpa(),reverse=True)
            top_student=dept_students[:3]
            print(f"Department: {dept}")
            print(f"Total Students: {len(dept_students)}")
        if dept_students:
            total_gpa=sum(student.calculate_gpa()for student in dept_students)
            average_gpa=total_gpa/len(dept_students)
        else:
            average_gpa=0
        print(f"Average GPA: {average_gpa:2f}")
        print("___Top Students___".center(50))
        rank=1
        for student in top_student:
            print(f"{rank}:"
                  f"{student.name:<20}"
                  f"{student.calculate_gpa():.2f}")
            rank+=1
        print()
    #Generate a report to display instructor's courses enrollment
    def enrollment_report(self):
        print("_"*50,"Enrollment Report","_"*50)
        print(
            f"{'Course':<12}"
            f"{'Capacity':<12}"
            f"{'Enrolled':<12}"
        )
        print("_"*100)
        for course in self.system.courses:
            print(f"{course.code:<12}"
                f"{course.capacity:<12}"
                f"{len(course.enrolled_students):<12}"
            )
        print("_" * 100)

    # Generate a report to display available seats in instructor's courses
    def available_seats_report(self):
        print("_"*50,"Available Seats Report","_"*50)
        (print(
            f"{'Course':<12}"
            f"{'Available':<12}"
        ))
        print("_"*100)
        available_courses=get_available_courses(self.system.courses)
        for course in available_courses:
            print(f"{course.code:<12}"
                f"{course.available_seats():<12}")
        print("_" * 100)

    def instructor_report_choice(self, report_choice):
        if report_choice == "1":
            self.enrollment_report()
        elif report_choice == "2":
            self.available_seats_report()
        elif report_choice == "3":
            self.students_insights()
        else:
            print("Please enter a valid choice")
            print()


