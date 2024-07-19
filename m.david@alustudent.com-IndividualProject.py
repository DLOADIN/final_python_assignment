import json
import urwid

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

    def add_student(self, names, email):
        student_details = Student(email, names)
        self.student_list.append(student_details)
        return f"Student {names} added successfully."

    def add_course(self, name, trimester, credits):
        course = Course(name, trimester, credits)
        self.course_list.append(course)
        return f"Course {name} added successfully."
    
    def register_student_for_course(self, student_names, course_name, grade):
        student = next((s for s in self.student_list if s.names == student_names), None)
        course = next((c for c in self.course_list if c.name == course_name), None)

        if student and course:
            student.register_for_course(course_name, grade)
            return f"{student_names} has been registered in the {course_name} course."
        else:
            return f"Couldn't register {student_names} in {course_name} course."

    def calculate_GPA(self):
        for student in self.student_list:
            student.calculate_GPA()

    def calculate_ranking(self):
        self.student_list.sort(key=lambda student: student.GPA, reverse=True)

    def search_by_grade(self, max_grade, min_grade):
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
        return "Data saved successfully."

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
            return "No saved data found."

    def display_lists(self):
        student_list = "Students:\n" + "\n".join([f"- {student.names} (Email: {student.email})" for student in self.student_list])
        course_list = "Courses:\n" + "\n".join([f"- {course.name} (Trimester: {course.trimester}, Credits: {course.credits})" for course in self.course_list])
        return f"{student_list}\n\n{course_list}"

class GradeBookUI:
    def __init__(self):
        self.gradebook = GradeBook()
        self.loop = None
        self.body = urwid.SimpleListWalker([])
        self.main_menu()

    def main_menu(self, button=None):
        menu_items = [
            "0. Display Lists",
            "1. Add Student",
            "2. Add Course",
            "3. Register Student for Course",
            "4. Calculate GPA for Students",
            "5. Calculate Student Rankings",
            "6. Search by GPA",
            "7. Save Data",
            "8. Load Data",
            "9. Exit"
        ]
        body = [urwid.Text("Welcome to the Grade Book Application"), urwid.Divider()]
        body.extend([urwid.Button(item, on_press=self.menu_choice, user_data=item[0]) for item in menu_items])
        self.body[:] = body

    def menu_choice(self, button, choice):
        if choice == "0":
            self.display_lists()
        elif choice == "1":
            self.add_student()
        elif choice == "2":
            self.add_course()
        elif choice == "3":
            self.register_student_for_course()
        elif choice == "4":
            self.calculate_gpa()
        elif choice == "5":
            self.calculate_ranking()
        elif choice == "6":
            self.search_by_grade()
        elif choice == "7":
            self.save_data()
        elif choice == "8":
            self.load_data()
        elif choice == "9":
            raise urwid.ExitMainLoop()

    def display_lists(self):
        text = self.gradebook.display_lists()
        self.show_text(text)

    def add_student(self):
        self.show_input_dialog("Enter student names:", self._add_student_name)

    def _add_student_name(self, names):
        self.show_input_dialog("Enter student email:", lambda email: self._add_student_email(names, email))

    def _add_student_email(self, names, email):
        result = self.gradebook.add_student(names, email)
        self.show_text(result)

    def add_course(self):
        self.show_input_dialog("Enter course name:", self._add_course_name)

    def _add_course_name(self, name):
        self.show_input_dialog("Enter trimester:", lambda trimester: self._add_course_trimester(name, trimester))

    def _add_course_trimester(self, name, trimester):
        self.show_input_dialog("Enter course credits:", lambda credits: self._add_course_credits(name, trimester, credits))

    def _add_course_credits(self, name, trimester, credits):
        try:
            credits = int(credits)
            result = self.gradebook.add_course(name, trimester, credits)
            self.show_text(result)
        except ValueError:
            self.show_text("Invalid credits. Please enter a number.")

    def register_student_for_course(self):
        self.show_input_dialog("Enter student names:", self._register_student_name)

    def _register_student_name(self, student_names):
        self.show_input_dialog("Enter course name:", lambda course_name: self._register_course_name(student_names, course_name))

    def _register_course_name(self, student_names, course_name):
        self.show_input_dialog("Enter grade:", lambda grade: self._register_grade(student_names, course_name, grade))

    def _register_grade(self, student_names, course_name, grade):
        try:
            grade = float(grade)
            result = self.gradebook.register_student_for_course(student_names, course_name, grade)
            self.show_text(result)
        except ValueError:
            self.show_text("Invalid grade. Please enter a number.")

    def calculate_gpa(self):
        self.gradebook.calculate_GPA()
        self.show_text("GPA calculated for all students.")

    def calculate_ranking(self):
        self.gradebook.calculate_ranking()
        text = "Students ranked by GPA:\n" + "\n".join([f"{student.names}: GPA {student.GPA}" for student in self.gradebook.student_list])
        self.show_text(text)

    def search_by_grade(self):
        self.show_input_dialog("Enter maximum GPA:", self._search_max_gpa)

    def _search_max_gpa(self, max_gpa):
        self.show_input_dialog("Enter minimum GPA:", lambda min_gpa: self._search_min_gpa(max_gpa, min_gpa))

    def _search_min_gpa(self, max_gpa, min_gpa):
        try:
            max_gpa = float(max_gpa)
            min_gpa = float(min_gpa)
            filtered_students = self.gradebook.search_by_grade(max_gpa, min_gpa)
            if filtered_students:
                text = "Filtered Students:\n" + "\n".join([f"{student.names}: GPA {student.GPA}" for student in filtered_students])
            else:
                text = "No students found in the specified GPA range."
            self.show_text(text)
        except ValueError:
            self.show_text("Invalid GPA. Please enter numbers.")

    def save_data(self):
        self.show_input_dialog("Enter filename to save data (e.g., gradebook.json):", self._save_data)

    def _save_data(self, filename):
        result = self.gradebook.save_to_file(filename)
        self.show_text(result)

    def load_data(self):
        self.show_input_dialog("Enter filename to load data (e.g., gradebook.json):", self._load_data)

    def _load_data(self, filename):
        result = GradeBook.load_from_file(filename)
        if isinstance(result, GradeBook):
            self.gradebook = result
            self.show_text("Data loaded successfully.")
        else:
            self.show_text(result)

    def show_text(self, text):
        self.body[:] = [urwid.Text(text), urwid.Divider(), urwid.Button("Back to Main Menu", on_press=self.main_menu)]

    def show_input_dialog(self, prompt, callback):
        edit = urwid.Edit(prompt + "\n")
        done = urwid.Button("OK")
        urwid.connect_signal(done, 'click', lambda button: self.dialog_done(edit, callback))
        self.body[:] = [edit, done]

    def dialog_done(self, edit, callback):
        callback(edit.edit_text)

    def run(self):
        list_box = urwid.ListBox(self.body)
        self.loop = urwid.MainLoop(urwid.Frame(list_box, header=urwid.Text("Grade Book Application", align='center')))
        self.loop.run()

def main():
    GradeBookUI().run()

if __name__ == "__main__":
    main()