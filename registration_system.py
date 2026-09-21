#This class is responsible for maintaining collections and coordinating operations across entities of the system
import re
import random


from student import (Student, validate_student_id, add_a_student)
from instructor import Instructor
from admin import Admin
from course import (
    add_a_course,
    validate_course_code,
    find_course,
    check_prerequisite_chain,
    get_available_courses,
    InvalidCourseCodeError,
    InvalidStudentIDError,
    InvalidInstructorIDError,
    StudentNotFoundError,
    CourseNotFoundError,
    InstructorNotFoundError,
    DuplicateEnrollmentError,
    CourseFullError,
    MissingPrerequisiteError,
)


def validate_instructor_id(instructor_id):
    pattern = r"^IN[0-9]{4}$"
    return re.match(pattern, instructor_id) is not None


def generate_instructor_id(existing_instructors):
    while True:
        number = random.randint(0, 9999)
        instructor_id = "IN" + str(number).zfill(4)

        if not validate_instructor_id(instructor_id):
            continue

        if any(i.id == instructor_id for i in existing_instructors):
            continue

        return instructor_id


def get_instructor_name():
    while True:
        name = input("Enter instructor name: ").strip()
        pattern = r"^[A-Za-z\s]+$"

        if name and re.match(pattern, name):
            return name

        print("Invalid name. Please use letters only.")


def get_instructor_email():
    while True:
        email = input("Enter instructor email: ")
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if re.match(pattern, email):
            return email

        print("Invalid email. Please enter a valid email.")


def add_an_instructor(existing_instructors):
    print("\n--- Add New Instructor ---")

    name = get_instructor_name()
    instructor_id = generate_instructor_id(existing_instructors)
    email = get_instructor_email()
    department = input("Enter department: ").strip()
    password = input("Enter password: ")

    print(f"Generated Instructor ID: {instructor_id}")

    return Instructor(name, instructor_id, email, password, department)



class RegistrationSystem:

    def __init__(self):
        #system entities
        self.students = []
        self.instructors = []
        self.courses = []
        self.admins = []

        self.create_default_admin()
    # ---------- lookup helpers (raise on bad input used by both menus) ----------

    def find_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student

        return None

    def find_instructor(self, instructor_id):
        for instructor in self.instructors:
            if instructor.id == instructor_id:
                return instructor

        return None

    def get_student(self, student_id):
        if not validate_student_id(student_id):
            raise InvalidStudentIDError(f"'{student_id}' is not a valid student ID.")

        student = self.find_student(student_id)

        if student is None:
            raise StudentNotFoundError(f"No student found with ID {student_id}.")

        return student

    def get_instructor(self, instructor_id):
        if not validate_instructor_id(instructor_id):
            raise InvalidInstructorIDError(f"'{instructor_id}' is not a valid instructor ID.")

        instructor = self.find_instructor(instructor_id)

        if instructor is None:
            raise InstructorNotFoundError(f"No instructor found with ID {instructor_id}.")

        return instructor

    def get_course(self, course_code):
        if not validate_course_code(course_code):
            raise InvalidCourseCodeError(f"'{course_code}' is not a valid course code.")

        course = find_course(course_code, self.courses)

        if course is None:
            raise CourseNotFoundError(f"No course found with code {course_code}.")

        return course

    #Checks whether the instructor has already a course in the same day and time
    def schedule_conflict(self,instructor,new_course):
        for course in self.courses:
            if course.instructor_id != instructor.id:
                continue
            if course.day!=new_course.day:
                continue
            if new_course.start_time<course.end_time and new_course.end_time>course.start_time:
                return True
        return False

    # ---------- registration (creating accounts) ----------

    def register_student(self):
        student = add_a_student(self.students)
        self.students.append(student)
        print("Student registered successfully.")
        print("-" * 100)
        return student

    def register_instructor(self):
        instructor = add_an_instructor(self.instructors)
        self.instructors.append(instructor)
        print("Instructor registered successfully.")
        print("-" * 100)
        return instructor

    def create_default_admin(self):
        admin=Admin("000000","System Admin","sic_admin@gmail.com","admin213")
        self.admins.append(admin)

    # ===================== INSTRUCTOR-ONLY ACTIONS =====================

    def add_course(self, instructor):
        course = add_a_course(self.courses)
        if self.schedule_conflict(instructor, course):
            print("Schedule conflict: Can\'t add this course")
            return None
        course.instructor_id = instructor.id
        self.courses.append(course)
        instructor.add_course(course.code)
        print(f"Course {course.code} added successfully.")
        print("-"*100)
        return course

    def remove_course(self, instructor):
        course_code = input("Enter course code to remove: ").strip().upper()

        try:
            course = self.get_course(course_code)

        except (InvalidCourseCodeError, CourseNotFoundError) as error:
            print(f"Not found: {error}")
            return

        if course.instructor_id != instructor.id:
            print("You can only remove courses you created.")
            return

        self.courses.remove(course)
        print(instructor.delete_course(course.code))
        print(f"Course {course.code} removed successfully.")
        print("-" * 100)

    def instructor_enroll_student(self, instructor):
        student_id = input("Enter student ID: ").strip().upper()
        course_code = input("Enter course code: ").strip().upper()

        try:
            student = self.get_student(student_id)
            course = self.get_course(course_code)

            if student not in instructor.students:
                print("You can only enroll students in your roster")
                return
            if course.code not in instructor.courses:
                print("You can only manage your assigned courses")
                return


            check_prerequisite_chain(course, student, self.courses)

            print(course.enroll_student(student.id))
            print(student.add_course(course.code))

        except (InvalidStudentIDError, InvalidCourseCodeError) as error:
            print(f"Invalid input: {error}")

        except (StudentNotFoundError, CourseNotFoundError) as error:
            print(f"Not found: {error}")

        except MissingPrerequisiteError as error:
            print(f"Enrollment failed: {error}")

        except DuplicateEnrollmentError as error:
            print(f"Enrollment failed: {error}")

        except CourseFullError as error:
            print(f"Enrollment failed: {error}")

    def instructor_drop_student(self, instructor):
        student_id = input("Enter student ID: ").strip().upper()
        course_code = input("Enter course code: ").strip().upper()

        try:
            student = self.get_student(student_id)
            course = self.get_course(course_code)

            if student not in instructor.students:
                print("You can only drop students in your roster")
                return
            if course.code not in instructor.courses:
                print("You can only manage your assigned courses")
                return

            print(student.drop_course(course.code))
            print(course.drop_student(student.id))

        except (InvalidStudentIDError, StudentNotFoundError) as error:
            print(f"Student Error: {error}")
            return

        except (InvalidCourseCodeError, CourseNotFoundError) as error:
            print(f"Course error: {error}")
            return

    def instructor_add_grade(self, instructor):
        student_id = input("Enter student ID: ").strip().upper()
        course_code = input("Enter course code: ").strip().upper()
        grade = input("Enter grade: ").strip().upper()

        try:
            student = self.get_student(student_id)
            course= self.get_course(course_code)

            if student.id not in course.enrolled_students:
                print("You can only add grades to students in this course.")
                return
            if course_code not in instructor.courses:
                print("You can only add grades to courses assigned to you.")
                return
            print(student.add_grade(course_code, grade))

        except (InvalidStudentIDError, StudentNotFoundError) as error:
            print(f"Student Error: {error}")
            return
        except(InvalidCourseCodeError,CourseNotFoundError) as error:
            print(f"Course Error: {error}")

    def add_student_to_instructor_roster(self, instructor):
        student_id = input("Enter student ID: ").strip().upper()
        try:
            student = self.get_student(student_id)
            print(instructor.add_student(student))
        except (InvalidStudentIDError, StudentNotFoundError) as error:
            print(f"Not found: {error}")

    def instructor_menu(self, instructor):
        while True:
            print(f"\n--- Instructor Menu ({instructor.name}) ---")
            print("1. Add course")
            print("2. Remove one of my courses")
            print("3. View my courses")
            print("4. View my students")
            print("5. Add a student to my roster")
            print("6. Enroll a student in a course")
            print("7. Drop a student from a course")
            print("8. Add a grade to a student")
            print("9. Log out")
            print("_" * 100)

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_course(instructor)
            elif choice == "2":
                self.remove_course(instructor)
            elif choice == "3":
                instructor.display_courses()
            elif choice == "4":
                instructor.display_students()
            elif choice == "5":
                self.add_student_to_instructor_roster(instructor)
            elif choice == "6":
                self.instructor_enroll_student(instructor)
            elif choice == "7":
                self.instructor_drop_student(instructor)
            elif choice == "8":
                self.instructor_add_grade(instructor)
            elif choice == "9":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")

    # ===================== STUDENT-ONLY ACTIONS =====================

    def show_available_courses(self):
        # filter: only courses that still have open seats
        available = get_available_courses(self.courses)

        if not available:
            print("No courses currently have available seats.")
            return

        print("\n--- Available Courses ---")
        for course in available:
            print(f"- {course.code}: {course.title} ({course.available_seats()} seats left)")

    def student_enroll(self, student):
        course_code = input("Enter course code: ").strip().upper()

        try:
            course = self.get_course(course_code)
            check_prerequisite_chain(course, student, self.courses)

            print(course.enroll_student(student.id))
            print(student.add_course(course.code))

        except InvalidCourseCodeError as error:
            print(f"Invalid input: {error}")

        except CourseNotFoundError as error:
            print(f"Not found: {error}")

        except MissingPrerequisiteError as error:
            print(f"Enrollment failed: {error}")

        except DuplicateEnrollmentError as error:
            print(f"Enrollment failed: {error}")

        except CourseFullError as error:
            print(f"Enrollment failed: {error}")

    def student_drop(self, student):
        course_code = input("Enter course code: ").strip().upper()

        try:
            course = self.get_course(course_code)

        except (InvalidCourseCodeError, CourseNotFoundError) as error:
            print(f"Not found: {error}")
            return

        print(student.drop_course(course.code))
        print(course.drop_student(student.id))
    #Displaying student's schedule using student iterator
    def show_schedule(self, student):
        print(f"\n--- Schedule for {student.name} ---")

        # Iterator: Student.__iter__ walks through the enrolled courses
        print("_"*50,f"{student.name}\'s Schedule","_"*50)
        print(f"{'Day':<12} | {'Time':<15} | {'Course':<10} | {'Title'}")
        print("-"*70)
        for course_code in student:
            course = find_course(course_code, self.courses)
            if course is not None:
                print(f"{course.day:<12} | {course.start_time}-{course.end_time:<15} | {course.code:<12} | {course.title}")
            else:
                print(f"course: {course_code} not found.")
    def student_menu(self, student):
        while True:
            print(f"\n--- Student Menu ({student.name}) ---")
            print("1. View available courses")
            print("2. Enroll in a course")
            print("3. Drop a course")
            print("4. View my schedule")
            print("5. View my grade report")
            print("6. Log out")
            print("_" * 100)

            choice = input("Choose an option: ")

            if choice == "1":
                self.show_available_courses()
            elif choice == "2":
                self.student_enroll(student)
            elif choice == "3":
                self.student_drop(student)
            elif choice == "4":
                self.show_schedule(student)
            elif choice == "5":
                student.grade_report()
            elif choice == "6":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")

    # ===================== ADMIN-ONLY ACTIONS =====================
    def display_all_students(self):
        if not self.students:
            print("No students registered.")
            return
        print("_"*50,"All Registered Students","_"*50)
        for student in self.students:
            student.display_info()
            print("_"*50)

    def display_all_instructors(self):
        if not self.instructors:
            print("No instructors registered.")
            return
        print("_"*50,"All Registered Instructors","_"*50)
        for instructor in self.instructors:
            instructor.display_info()
            print("_"*50)

    def display_all_courses(self):
        if not self.courses:
            print("No courses available.")
            return
        print("_"*60,"All Courses","_"*60)
        for course in self.courses:
            course.display_info()
            print("_"*50)

    def display_system_statistics(self):
        total_enrollments = sum(len(course.enrolled_students)for course in self.courses)
        print("_"*50,"System Statistics","_"*50)
        print(
              f"Total Students: {len(self.students)}\n"
              f"Total Instructors: {len(self.instructors)}\n"
              f"Total Courses: {len(self.courses)}\n"
              f"Total Admins: {len(self.admins)}\n"
              f"Total Enrollments: {total_enrollments}\n"
              )

    def admin_add_course(self):

        course = add_a_course(self.courses)

        instructor_id = input(
            "Enter instructor ID to assign this course: "
        ).strip().upper()

        try:
            instructor = self.get_instructor(instructor_id)
            if self.schedule_conflict(instructor, course):
                print("Schedule conflict: Can't assign this course to the instructor.")
                return

        except (InvalidInstructorIDError, InstructorNotFoundError) as error:
            print(f"Unable to assign instructor: {error}")
            return

        course.instructor_id = instructor.id
        self.courses.append(course)
        instructor.add_course(course.code)
        print(
            f"Course {course.code} added successfully "
            f"and assigned to {instructor.name}."
        )

        return course

    def admin_remove_course(self):

        course_code = input(
            "Enter course code to remove: "
        ).strip().upper()

        try:
            course = self.get_course(course_code)

        except (InvalidCourseCodeError, CourseNotFoundError) as error:
            print(f"Not found: {error}")
            return

        instructor = None

        if course.instructor_id is not None:
            instructor = self.find_instructor(course.instructor_id)

        self.courses.remove(course)

        if instructor is not None:
            instructor.delete_course(course.code)

        print(f"Course {course.code} removed successfully.")


