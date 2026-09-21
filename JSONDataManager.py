#Converts Python objects to JSON-compatible data when saving
import json
from datetime import datetime
from student import Student
from instructor import Instructor
from admin import Admin
from course import Course

class JSONDataManager:
    def __init__(self,filename="university_data.json"):
        self.filename = filename

    # Serialize the current system state and save it to the JSON file
    def save_data(self,system):
        data={
            "students":[],
            "instructors":[],
            "courses":[],
            "admins":[]
        }
        for student in system.students:
            data["students"].append({
                "id":student.id,
                "name":student.name,
                "email":student.email,
                "password":student.password,
                "dept":student.dept,
                "courses":student.courses,
                "grades":student.grades,
            })

        for instructor in system.instructors:
            data["instructors"].append({
                "id":instructor.id,
                "name":instructor.name,
                "email":instructor.email,
                "password":instructor.password,
                "dept":instructor.dept,
                "courses":instructor.courses,
                "students":[student.id for student in instructor.students],
            })

        for course in system.courses:
            data["courses"].append({
                "code":course.code,
                "title":course.title,
                "capacity":course.capacity,
                "prerequisites":course.prerequisites,
                "instructor_id":course.instructor_id,
                "enrolled_students":course.enrolled_students,
                "day":course.day,
                "start_time":course.start_time.strftime("%H:%M")if course.start_time else None,
                "end_time":course.end_time.strftime("%H:%M")if course.end_time else None,
            })

        for admin in system.admins:
            data["admins"].append({
                "id":admin.id,
                "name":admin.name,
                "email":admin.email,
                "password":admin.password,
                "dept":admin.dept,
            })


        with open(self.filename,"w") as file:
            json.dump(data,file,indent=4)

    # Reconstruct Python objects from the saved JSON data
    def load_data(self, system):

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        #students section

        system.students=[]

        for student_data in data.get("students",[]):
            student = Student(
                student_data["name"],
                student_data["id"],
                student_data["email"],
                student_data["password"],
                student_data["dept"]
            )

            student.courses=student_data.get("courses",[])
            student.grades=student_data.get("grades",{})

            system.students.append(student)

        #instructors section

        system.instructors = []

        for instructor_data in data.get("instructors", []):
            instructor = Instructor(
                instructor_data["name"],
                instructor_data["id"],
                instructor_data["email"],
                instructor_data["password"],
                instructor_data["dept"]
            )

            instructor.courses = instructor_data.get(
                "courses", []
            )

            system.instructors.append(instructor)

        #courses section

        system.courses = []

        for course_data in data.get("courses", []):

            start_time = None
            end_time = None

            if course_data.get("start_time"):
                start_time = datetime.strptime(
                    course_data["start_time"],
                    "%H:%M"
                ).time()

            if course_data.get("end_time"):
                end_time = datetime.strptime(
                    course_data["end_time"],
                    "%H:%M"
                ).time()

            course = Course(
                course_data["code"],
                course_data["title"],
                course_data["capacity"],
                course_data.get("prerequisites", []),
                course_data.get("instructor_id"),
                course_data.get("day"),
                start_time,
                end_time
            )

            course.enrolled_students = course_data.get(
                "enrolled_students", []
            )

            system.courses.append(course)

        #linking instructors with students

        for instructor_data in data.get("instructors", []):

            instructor = system.find_instructor(
                instructor_data["id"]
            )

            for student_id in instructor_data.get(
                    "students", []
            ):

                student = system.find_student(student_id)

                if student is not None:
                    instructor.students.append(student)


        #admin section

        system.admins = []

        for admin_data in data.get("admins", []):
            admin = Admin(
                admin_data["id"],
                admin_data["name"],
                admin_data["email"],
                admin_data["password"],
                admin_data["dept"]
            )

            system.admins.append(admin)



