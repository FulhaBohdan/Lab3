import json

class Person:
    def __init__(self, id: int, name: str, surname: str):
        self.first_name = name
        self.last_name = surname
        self.id_number = id

    def get_info(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id_number})"

class Student(Person):
    def __init__(self, id: int, name: str, surname: str):
        super().__init__(id, name, surname)
        self.courses = []

    def add_course(self, course_name: str):
        if course_name not in self.courses:
            self.courses.append(course_name)

    def get_courses(self):
        return self.courses


class Teacher(Person):
    def __init__(self, id: int, name: str, surname: str):
        super().__init__(id, name, surname)
        self.courses = []

    def assign_course(self, course_name: str):
        if course_name not in self.courses:
            self.courses.append(course_name)

    def get_courses(self):
        return self.courses


class Course:
    def __init__(self, code: str, course_name: str, description: str, teacher: Teacher):
        self.name = course_name
        self.description = description
        self.course_id = code
        self.teacher = teacher
        self.students = []

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)
            student.add_course(self.name)

    def get_students(self):
        return [student.get_info() for student in self.students]


class University:
    def __init__(self, name: str):
        self.name = name
        self.students = []
        self.teachers = []
        self.courses = []

    def add_student(self, student: Student):
        self.students.append(student)

    def add_teacher(self, teacher: Teacher):
        self.teachers.append(teacher)

    def add_course(self, course: Course):
        self.courses.append(course)

    def find_student(self, student_id: int):
        for student in self.students:
            if student.id_number == student_id:
                return student
        return None

    def find_teacher(self, teacher_id: int):
        for teacher in self.teachers:
            if teacher.id_number == teacher_id:
                return teacher
        return None

    def find_course(self, course_id: str):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    def register_student_to_course(self, student: Student, course: Course):
        if student in self.students and course in self.courses:
            course.add_student(student)

    def save_to_file(self, filename="university_data.json"):
        data = {
            "name": self.name,
            "students": [vars(s) for s in self.students],
            "teachers": [vars(t) for t in self.teachers],
            "courses": [
                {
                    "name": c.name,
                    "description": c.description,
                    "course_id": c.course_id,
                    "teacher_id": c.teacher.id_number,
                    "student_ids": [s.id_number for s in c.students]
                } for c in self.courses
            ]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("Дані збережено!")

    def load_from_file(self, filename="university_data.json"):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.name = data["name"]
        self.students = [Student(s["id_number"], s["first_name"], s["last_name"]) for s in data["students"]]
        self.teachers = [Teacher(t["id_number"], t["first_name"], t["last_name"]) for t in data["teachers"]]

        id_to_student = {s.id_number: s for s in self.students}
        id_to_teacher = {t.id_number: t for t in self.teachers}

        self.courses = []
        for c in data["courses"]:
            teacher = id_to_teacher.get(c["teacher_id"])
            course = Course(c["course_id"], c["name"], c["description"], teacher)
            for sid in c["student_ids"]:
                student = id_to_student.get(sid)
                if student:
                    course.add_student(student)
            self.courses.append(course)




if __name__ == "__main__":
    uni = University("Tech University")

    # Додати викладачів
    t1 = Teacher(111, "Meryl", "Brown")
    t2 = Teacher(112, "John", "Smith")
    uni.add_teacher(t1)
    uni.add_teacher(t2)

    # Додати студентів
    s1 = Student(101, "Adam", "Miller")
    s2 = Student(102, "Emma", "O'Neil")
    uni.add_student(s1)
    uni.add_student(s2)

    # Додати курси
    c1 = Course("CS125", "Intro to Python", "KN", t1)
    c2 = Course("CS111", "OOP", "IPZ", t2)
    uni.add_course(c1)
    uni.add_course(c2)

    # Реєстрація
    uni.register_student_to_course(s1, c1)
    uni.register_student_to_course(s2, c1)
    uni.register_student_to_course(s2, c2)

    # Зберегти
    uni.save_to_file()

    # Завантажити
    new_uni = University("DRAHO")
    new_uni.load_from_file()

    # Вивести студентів з курсу
    for course in new_uni.courses:
        print(f"Course: {course.name}")
        print("Students:", course.get_students())
