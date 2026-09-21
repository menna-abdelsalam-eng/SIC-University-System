from person import Person
class Instructor(Person):

    def __init__(self, name, id, email, password, dept):
        super().__init__(id, name, email, password,dept)# MODIFIED
        self.courses = []
        self.students = []

    def get_role(self):
        return "Instructor"

    def add_course(self, course_code):
        if course_code in self.courses:
            return "Course already assigned."
        self.courses.append(course_code)
        return "Course added successfully."

    def delete_course(self, course_code):
        if course_code not in self.courses:
            return "Course not found."
        self.courses.remove(course_code)
        return "Course deleted successfully."

    def display_courses(self):
        print("Courses:")
        if not self.courses:
            return "No courses assigned."
        for course in self.courses:
            print("- " + course)

    def add_student(self, student):
        if student in self.students:
            return "Student is already in your roster."
        self.students.append(student)
        return "Student added to your roster successfully."

    def delete_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                self.students.remove(student)
                return "Student removed from your roster successfully."
        return "Student not found in your roster."

    def display_students(self):
        if not self.students:
            print("No students in your roster.")
            return
        print("--- Students ---")
        for student in self.students:
            print(f"Name: {student.name}")
            print(f"ID: {student.id}")
            print(f"Email: {student.email}")
            print(f"Department: {student.dept}")
            print("-"*30)


    def display_info(self):
        print("--- Instructor Information ---")
        print(f"Name: {self.name}")
        print(f"ID: {self.id}")
        print(f"Email: {self.email}")
        print(f"Department: {self.dept}")
        print("-"*100)

