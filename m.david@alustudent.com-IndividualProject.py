import json

class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = []
        self.GPA = 0.0

    
    def calculate_GPA(self):
        if not self.courses_registered:
            return self.GPA
        total_gpa = 0.0
        for course_dict in self.courses_registered: 
            for grade in course_dict.values():
                gpa = grade * 4 / 100
                total_gpa += gpa
        self.GPA = total_gpa / len(self.courses_registered)
        return self.GPA

     # def calculate_GPA(self):
    # if not self.courses_registered:
    #     return self.GPA
    
    # total_gpa = 0.0
    # for course_dict in self.courses_registered:
    #     for grade in course_dict.values():
    #         gpa = grade * 4 / 100  
    #         total_gpa += gpa
    
    # self.GPA = total_gpa / len(self.courses_registered)
    # return self.GPA
    # def calculate_GPA(self):
    # if not self.courses_registered:
    #     return self.GPA
    # elif:
    #     for grade in self.courses_registered:
    #         self.GPA = grade * 4 / 100
    # return self.GPA


    def register_for_course(self, course_name, grade):
        course_dict = {course_name: grade}
        self.courses_registered.append(course_dict)

    def to_dict(self):
        return {
            'email': self.email,
            'names': self.names,
            'courses_registered': self.courses_registered,
            'GPA': self.GPA
        }

    @staticmethod
    def from_dict(data):
        student = Student(data['email'], data['names'])
        student.courses_registered = data['courses_registered']
        student.GPA = data['GPA']
        return student

class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits

    def to_dict(self):
        return {
            'name': self.name,
            'trimester': self.trimester,
            'credits': self.credits
        }

    @staticmethod
    def from_dict(data):
        return Course(data['name'], data['trimester'], data['credits'])

class GradeBook:
    def __init__(self):
        self.course_list = []
        self.student_list = []

    def add_student(self):
        names = input("Please Enter your names: ")
        email = input("Please Enter your email: ")
        student_details = Student(email, names)
        self.student_list.append(student_details)
        print(f"Student {names} added successfully.")

    def add_course(self):
        name = input("Enter course name: ")
        trimester = input("Enter trimester: ")
        credits = int(input("Enter course credits: "))
        course = Course(name, trimester, credits)
        self.course_list.append(course)
        print(f"Course {name} added successfully.")
    
    def register_student_for_course(self):
        student_names = input("Enter your names: ")
        course_name = input("Enter the course name you want to register for: ")
        student = next((s for s in self.student_list if s.names == student_names), None)
        course = next((c for c in self.course_list if c.name == course_name), None)

        if student and course:
            grade = float(input("Enter your grade: "))
            student.register_for_course(course_name, grade)
            print(f"{student_names} has been registered in the {course_name} course.")
        else:
            print(f"Couldn't register {student_names} in {course_name} course.")

    def calculate_GPA(self):
        for student in  self.student_list:
            student.calculate_GPA()

    def calculate_ranking(self):
        self.student_list.sort(key=lambda student: student.GPA, reverse=True)

    def search_by_grade(self):
        max_grade = float(input("Enter your maximum GPA: "))
        min_grade = float(input("Enter your minimum GPA: "))
        filtered_students = []
        for student in self.student_list:
            if min_grade <= student.GPA <= max_grade:
                filtered_students.append(student)
        return filtered_students

    def save_to_file(self, filename):
        data = {
            'students': [student.to_dict() for student in self.student_list],
            'courses': [course.to_dict() for course in self.course_list]
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print("Data saved successfully.")

    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                gradebook = GradeBook()
                gradebook.student_list = [Student.from_dict(s) for s in data['students']]
                gradebook.course_list = [Course.from_dict(c) for c in data['courses']]
                return gradebook
        except FileNotFoundError:
            print("No saved data found.")
            return GradeBook()

def main():
    gradebook = GradeBook()

    while True:
        print("\nWelcome to the Grade Book Application")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Calculate GPA for Students")
        print("5. Calculate Student Rankings")
        print("6. Search by GPA")
        print("7. Save Data")
        print("8. Load Data")
        print("9. Exit")

        choice = input("Please select an option (1-9): ")

        if choice == "1":
            gradebook.add_student()
        elif choice == "2":
            gradebook.add_course()
        elif choice == "3":
            gradebook.register_student_for_course()
        elif choice == "4":
            gradebook.calculate_GPA()
            print("GPA calculated for all students.")
        elif choice == "5":
            gradebook.calculate_ranking()
            print("Students ranked by GPA:")
            for student in gradebook.student_list:
                print(f"{student.names}: GPA {student.GPA}")
        elif choice == "6":
            filtered_students = gradebook.search_by_grade()
            if filtered_students:
                print("Filtered Students:")
                for student in filtered_students:
                    print(f"{student.names}: GPA {student.GPA}")
            else:
                print("No students found in the specified GPA range.")
        elif choice == "7":
            filename = input("Enter filename to save data (e.g., gradebook.json): ")
            gradebook.save_to_file(filename)
        elif choice == "8":
            filename = input("Enter filename to load data (e.g., gradebook.json): ")
            gradebook = GradeBook.load_from_file(filename)
        elif choice == "9":
            print("Exiting the Grade Book Application. Goodbye!")
            exit()
        else:
            print("Invalid option, please select again.")

if __name__ == "__main__":
    main()
