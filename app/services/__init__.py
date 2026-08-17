from app.services.student import (
    StudentService,
    StudentNotFoundError,
    MajorNotFoundError,
    NoFieldsToUpdateError
)

from app.services.course import (
    CourseService,
    CourseNotFoundError,
    PrerequisiteCourseNotFoundError,
    CourseCannotBeOwnPrerequisiteError,
    CourseNoFieldsToUpdateError,
    CourseHasDependenciesError
)