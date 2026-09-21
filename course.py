import re
import random
from datetime import datetime

#Custom Exceptions for handling errors
class InvalidCourseCodeError(Exception):
    pass


class InvalidStudentIDError(Exception):
    pass


class StudentNotFoundError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class InvalidInstructorIDError(Exception):
    pass


class InstructorNotFoundError(Exception):
    pass


class DuplicateEnrollmentError(Exception):
    pass


class CourseFullError(Exception):
    pass


class MissingPrerequisiteError(Exception):
    pass


class Course:
    #initializing course information
    def __init__(self, code, title, capacity, prerequisites=None, instructor_id=None,day=None,start_time=None,end_time=None):
        self.code = code
        self.title = title
        self.capacity = capacity
        self.prerequisites = prerequisites if prerequisites else []
        self.instructor_id = instructor_id
        self.enrolled_students = []
        #displaying day and time
        self.day=day
        self.start_time=start_time
        self.end_time=end_time


    #Return the number of available seats in a course
    def available_seats(self):
        seat_checker = create_seat_checker(self.capacity)
        return seat_checker(len(self.enrolled_students))

    def is_full(self):
        return self.available_seats() <= 0

    def enroll_student(self, student_id):
        if student_id in self.enrolled_students:
            raise DuplicateEnrollmentError(
                f"Student {student_id} is already enrolled in {self.code}."
            )

        if self.is_full():
            raise CourseFullError(f"Course {self.code} is full.")

        self.enrolled_students.append(student_id)
        return f"Student {student_id} enrolled in {self.code} successfully."

    def drop_student(self, student_id):
        if student_id not in self.enrolled_students:
            return f"Student {student_id} is not enrolled in {self.code}."

        self.enrolled_students.remove(student_id)
        return f"Student {student_id} dropped from {self.code} successfully."

    def display_info(self):
        print("\n--- Course Information ---")
        print(f"Code: {self.code}")
        print(f"Title: {self.title}")
        print(f"Capacity: {self.capacity}")
        print(f"Available Seats: {self.available_seats()}")
        print("_" * 100)

        if not self.prerequisites:
            print("Prerequisites: None")
        else:
            print("Prerequisites: " + ", ".join(self.prerequisites))

        print(f"Enrolled Students: {len(self.enrolled_students)}")


def create_seat_checker(capacity):
    # Closure: remembers this course's capacity and reports remaining seats
    def check_seats(enrolled_count):
        return capacity - enrolled_count

    return check_seats


def validate_course_code(course_code):
    pattern = r"^[A-Z]{2,4}[0-9]{3}$"
    return re.match(pattern, course_code) is not None


def generate_course_code(existing_courses, subject):
    while True:
        number = random.randint(100, 999)
        course_code = subject.upper() + str(number)

        if not validate_course_code(course_code):
            continue

        if any(c.code == course_code for c in existing_courses):
            continue

        return course_code


def get_course_subject():
    while True:
        subject = input("Enter course subject code (e.g. CS, MATH): ").strip()

        if subject and re.match(r"^[A-Za-z]{2,4}$", subject):
            return subject

        print("Invalid subject. Please use 2-4 letters only.")


def get_course_title():
    while True:
        title = input("Enter course title: ").strip()

        if title:
            return title

        print("Invalid title. Please enter a non-empty title.")


def get_course_capacity():
    while True:
        capacity = input("Enter course capacity: ")

        if capacity.isdigit() and int(capacity) > 0:
            return int(capacity)

        print("Invalid capacity. Please enter a positive number.")


def get_course_prerequisites():
    prerequisites = []

    while True:
        prereq = input("Enter prerequisite course code (leave blank to stop): ").strip().upper()

        if prereq == "":
            break

        if not validate_course_code(prereq):
            print("Invalid course code format.")
            continue

        prerequisites.append(prereq)

    return prerequisites


def find_course(course_code, courses):
    for course in courses:
        if course.code == course_code:
            return course

    return None


def check_prerequisite_chain(course, student, courses):
    # Recursion: walks down each prerequisite's own prerequisites
    if not course.prerequisites:
        return True

    for prereq_code in course.prerequisites:
        grade = student.grades.get(prereq_code)

        if grade is None or grade == "F":
            raise MissingPrerequisiteError(
                f"Student {student.id} is missing prerequisite "
                f"{prereq_code} for {course.code}."
            )

        prereq_course = find_course(prereq_code, courses)

        if prereq_course is not None:
            check_prerequisite_chain(prereq_course, student, courses)

    return True


def get_available_courses(courses):
    # filter: only courses that still have open seats
    return list(filter(lambda course: not course.is_full(), courses))

def get_course_day():
    while True:
        day = input("Enter course day: ").strip().title()
        days_of_the_week = ["Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday"]
        if day in days_of_the_week:
            return day
        print("Invalid day. Please enter a valid day")

def get_course_time(input_time):

    while True:
        course_time=input(input_time).strip()
        try:
            return datetime.strptime(course_time, "%H:%M").time()
        except ValueError:
            print("Invalid time. Please enter a valid time")

def add_a_course(existing_courses):
    print("\n--- Add New Course ---")

    subject = get_course_subject()
    course_code = generate_course_code(existing_courses, subject)
    title = get_course_title()
    capacity = get_course_capacity()

    print(f"Generated Course Code: {course_code}")

    prerequisites = get_course_prerequisites()

    day=get_course_day()
    start_time=get_course_time("Enter Start Time i.e:(12:00): ")
    while True:
        end_time = get_course_time("Enter End Time i.e:(12:00): ")
        if end_time>start_time:
            break
        print("End time must be after start time")
    return Course(course_code,title,capacity,prerequisites,day=day,start_time=start_time,end_time=end_time)

