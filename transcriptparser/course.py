class Course:
    def __init__(self, course_code: str, sks_count: int, grade: str):
        self.course_code: str = course_code
        self.sks_count: int = sks_count
        self.grade: str = grade

    def __str__(self):
        return self.course_code + ' - ' + str(
            self.sks_count) + ' - ' + self.grade
