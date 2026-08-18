class NoFieldsToUpdateError(Exception):

    def __init__(self, student_id: int):
        self.student_id = student_id

        self.message = (
            f"No fields were provided to update "
            f"student with id {student_id}"
        )

        super().__init__(self.message)