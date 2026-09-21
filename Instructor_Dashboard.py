from instructor import *
from course import *
from datetime import datetime


class Instructor_Dashboard:
    def __init__(self,instructor,system):
        self.instructor = instructor
        self.system = system

    def dashboard_menu(self):
        while True:
            now=datetime.now()
            print("-"*100)
            print("_"*50,f"Dr.{self.instructor.name}\'s Dashboard","_"*50)
            print("-" * 100)
            print(f"Date: {now.strftime('%d/%m/%Y')}")
            print(f"Time: {now.strftime('%I:%M %p')}")
            print("-" * 100)
            print("1. View My Schedule\n"
                  "2. View Courses Statistics\n"
                  "3. View My Rank\n"
                  "4. Back to Secondary Menu\n")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.instructor_schedule()
            elif choice == "2":
                self.courses_statistics()
            elif choice == "3":
                self.instructor_rank()
            elif choice == "4":
                print("Back to Secondary Menu")
                break
            else:
                print("Invalid Choice")

    # Display the instructor's assigned courses and their schedules
    def instructor_schedule(self):
        print("My Courses".center(50))
        print("-"*100)
        for course_code in self.instructor.courses:
            course=find_course(course_code,self.system.courses)
            if course:
                print(f"{course.code:<10}"
                      f"{course.title:<25}"
                      f"{course.day:<12}"
                      f"{course.start_time}-{course.end_time}")


    # Calculate quick statistics for the instructor's courses and students
    def courses_statistics(self):
        print("Quick Statistics".center(50))
        print("-"*100)
        print(f"{'My Courses:':<25} {len(self.instructor.courses)}")
        print(f"{'My Students:':<25}{len(self.instructor.students)}")

        total_seats=0
        for course_code in self.instructor.courses:
            course=find_course(course_code,self.system.courses)
            if course:
                total_seats+=course.available_seats()
        print(f"{'Available Seats:':<25}{total_seats}")

        if self.instructor.students:
            total_gpa=sum(student.calculate_gpa() for student in self.instructor.students)
            average_gpa=total_gpa/len(self.instructor.students)
        else:
            average_gpa=0
        print(f"{'Students Average GPA:':<25}{average_gpa:.2f}")
        print("-"*100)

    # Rank instructors according to the average GPA of their students
    def instructor_rank(self):
        instructors_gpa = []

        for instructor in self.system.instructors:

            if instructor.students:
                total_gpa = sum(
                    student.calculate_gpa()
                    for student in instructor.students
                )
                average_gpa = total_gpa / len(instructor.students)
            else:
                average_gpa = 0

            instructors_gpa.append((instructor, average_gpa))

        instructors_gpa.sort(
            key=lambda item: item[1],
            reverse=True
        )

        rank = 1

        for instructor, average_gpa in instructors_gpa:
            if instructor.id == self.instructor.id:
                break
            rank += 1

        print("-" * 100)
        print(
            f"{'My Ranking:':<25}: "
            f"{rank}/{len(self.system.instructors)} Instructors"
        )
        print("-" * 100)







