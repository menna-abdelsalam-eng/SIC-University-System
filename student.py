#Subclass inherited from Person
import re
import random
from person import Person

#Processing a student's registered courses by using (iterator)
class StudentCourseIterator:
    def __init__(self, courses):
        self.courses = courses
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.courses):
            course = self.courses[self.index]
            self.index += 1
            return course
        raise StopIteration


class Student(Person):

    def __init__(self, name, id, email, password,dept):
        super().__init__(id, name, email, password,dept)
        #initializing student-specific attributes
        self.courses = []
        self.grades = {}

    #implementing polymorphism through overriding the method
    def get_role(self):
        return "Student"

    #Adding courses to student registered courses
    def add_course(self, course_code):
        #Avoiding Duplicates in registered courses
        if course_code in self.courses:
            return ("Student is already enrolled in this course.")

        self.courses.append(course_code)
        return ("Student enrolled in course successfully.")

    #Removing courses from student registered courses
    def drop_course(self, course_code):
        if course_code not in self.courses:
            return ("Student is not enrolled in this course.")

        self.courses.remove(course_code)

        if course_code in self.grades:
            del self.grades[course_code]

        return ("Student dropped course successfully.")

    def display_courses(self):
        if not self.courses:
            print("This student has no registered courses.")
            return

        print("Registered Courses:")
        for course in self.courses:
            print(f"- {course}")

    #Validating grade input value
    def validate_grade(self, grade):
        valid_grades = [
            "A+", "A", "A-", "B+", "B", "B-",
            "C+", "C", "C-", "D", "F"
        ]

        return grade in valid_grades

    #Updating student's grade if the student is enrolled in this course
    def add_grade(self, course_code, grade):
        if course_code not in self.courses:
            return ("Student is not enrolled in this course.")

        if not self.validate_grade(grade):
            return ("Invalid grade.")

        self.grades[course_code] = grade
        return ("Grade added successfully.")

    def calculate_gpa(self):

        grade_points = {
            "A+": 4.0, "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D": 1.0, "F": 0.0
        }

        gpa_calculator = create_gpa_calculator(grade_points)

        return gpa_calculator(list(self.grades.values()))

    def display_info(self):

        print("\n--- Student Information ---")
        print(f"Name: {self.name}")
        print(f"ID: {self.id}")
        print(f"Email: {self.email}")
        print(f"Department: {self.dept}")
        print("_"*100)

        if not self.courses:
            print("Courses: This student has no registered courses.")
        else:
            print("Courses:")
            print("_"*100)
            for course in self.courses:
                print(f"- {course}")

        print(f"GPA: {self.calculate_gpa():.2f}")

    def __iter__(self):
        return StudentCourseIterator(self.courses)

    #Displaying a student-grade report
    def grade_report(self):
        print("_" * 50, f"{self.name}\'s Grade Report", "_" * 50)
        if not self.grades:
            print("No grades available.")
            return
        print(f"{'Course':<20} | {'Grade':<20}")
        print("-" * 100)
        for course_code, grade in self.grades.items():
            print(f"{course_code:<20} | {grade:<20}")
        print("-" * 100)
        print(f"GPA: {self.calculate_gpa():.2f}")
        print("_" * 100)

#Creating a calculator that applies Closure through remembering grade_point
def create_gpa_calculator(grade_points):
    #inner function that uses grade_points from the enclosing function
    def calculate_gpa(grades):

        if len(grades) == 0:
            return 0

        total = 0

        for grade in grades:
            total += grade_points.get(grade, 0)
        return total / len(grades)
    return calculate_gpa

def get_student_email():
    while True:

        email = input("Enter student email: ")

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if re.match(pattern, email):
            return email

        print("Invalid email. Please enter a valid email.")


def validate_student_id(student_id):
    pattern = r"^ST[0-9]{4}$"

    return re.match(pattern, student_id) is not None

#Generate a student id with a specified pattern
def generate_student_id(existing_students):
    while True:

        number = random.randint(0, 9999)

        student_id = "ST" + str(number).zfill(4)

        if not validate_student_id(student_id):
            continue

        if any(s.id == student_id for s in existing_students):
            continue

        return student_id


def get_student_name():
    while True:

        name = input("Enter student name: ").strip()

        pattern = r"^[A-Za-z\s]+$"

        if name and re.match(pattern, name):
            return name

        print("Invalid name. Please use letters only.")


def add_a_student(existing_students):
    print("\n--- Add New Student ---")

    name = get_student_name()

    student_id = generate_student_id(existing_students)

    email = get_student_email()

    password = input("Enter password: ")

    dept=input("Enter department: ").upper()

    print(f"Generated Student ID: {student_id}")

    return Student(name, student_id, email, password,dept)

