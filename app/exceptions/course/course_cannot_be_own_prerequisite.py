class CourseCannotBeOwnPrerequisiteError(Exception):

    def __init__(
        self,
        course_id: int,
        prerequisite_course_id: int
    ):
        self.course_id = course_id
        self.prerequisite_course_id = prerequisite_course_id

        self.message = (
            f"Course with id {course_id} cannot use "
            f"course with id {prerequisite_course_id} "
            f"as its own prerequisite"
        )

        super().__init__(self.message)