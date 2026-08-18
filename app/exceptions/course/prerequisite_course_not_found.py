class PrerequisiteCourseNotFoundError(Exception):

    def __init__(self, prerequisite_course_id: int):
        self.prerequisite_course_id = prerequisite_course_id

        self.message = (
            f"Prerequisite course with id "
            f"{prerequisite_course_id} was not found"
        )

        super().__init__(self.message)