class CourseNotFoundError(Exception):

    def __init__(self, course_id: int):
        self.course_id = course_id

        self.message = (
            f"Course with id {course_id} was not found"
        )

        super().__init__(self.message)