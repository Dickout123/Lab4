class SchoolEnrollmentService:

    def __init__(self, max_students_per_class=1):
        self.classes = {
            '1-A': [], '1-B': [], '2-A': [], '2-B': []
        }
        self.max_students = max_students_per_class

    def add_student(self, student_name, grade):
        if not isinstance(student_name, str) or not student_name.strip():
            raise ValueError("Ім'я дитини не може бути порожнім.")

        target_classes = sorted([name for name in self.classes if name.startswith(f'{grade}-')])
        if not target_classes:
            raise KeyError(f"Клас для {grade} року не знайдено.")

        best_class = None
        min_students = self.max_students + 1

        for class_name in target_classes:
            current_count = len(self.classes[class_name])
            if current_count < min_students:
                min_students = current_count
                best_class = class_name

        if min_students > self.max_students:
            raise Exception(f"Немає місць у {grade} класі. Всі класи заповнені.")

        self.classes[best_class].append(student_name)
        return best_class

    def remove_student(self, student_name):
       
        for class_name, roster in self.classes.items():
            if student_name in roster:
                roster.remove(student_name)
                return True 
        return False  

    def get_class_roster(self, class_name):
        if class_name not in self.classes:
            raise KeyError(f"Клас '{class_name}' не існує.")
        return self.classes[class_name]

    def get_total_students(self):
        return sum(len(roster) for roster in self.classes.values())

if __name__ == '__main__':
    service = SchoolEnrollmentService(max_students_per_class=2)
    try:
        print("Додавання дітей:")
        print(f"Іван: {service.add_student('Іван Петренко', 1)}")
        print(f"Марія: {service.add_student('Марія Іванова', 1)}")
        print(f"Олег: {service.add_student('Олег Сидоренко', 2)}")

        print("\nСписки класів:")
        print(f"1-A: {service.get_class_roster('1-A')}")
        print(f"1-B: {service.get_class_roster('1-B')}")

        print("\nСпроба додати третього учня:")
        print(f"Анна: {service.add_student('Анна Коваленко', 1)}")

    except Exception as e:
        print(f"\nВиникла помилка: {e}")
