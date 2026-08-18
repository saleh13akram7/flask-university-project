class CourseHasDependenciesError(Exception):

    def __init__(
        self,
        course_id: int,
        dependencies: list[str]
    ):
        self.course_id = course_id
        self.dependencies = dependencies

        dependencies_text = ", ".join(dependencies)

        self.message = (
            f"Course with id {course_id} cannot be deleted "
            f"because it has dependencies: {dependencies_text}"
        )

        super().__init__(self.message)