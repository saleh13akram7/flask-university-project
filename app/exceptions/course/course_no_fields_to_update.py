class CourseNoFieldsToUpdateError(Exception):

    def __init__(self, course_id: int):
        self.course_id = course_id

        self.message = (
            f"No fields were provided to update "
            f"course with id {course_id}"
        )

        super().__init__(self.message)