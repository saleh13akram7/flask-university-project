class StudentNotFoundError(Exception):

    def __init__(self, student_id: int):
        self.student_id = student_id

        self.message = (
            f"Student with id {student_id} was not found"
        )

        super().__init__(self.message)