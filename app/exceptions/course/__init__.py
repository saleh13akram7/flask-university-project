from app.exceptions.course.course_not_found import (
    CourseNotFoundError
)

from app.exceptions.course.prerequisite_course_not_found import (
    PrerequisiteCourseNotFoundError
)

from app.exceptions.course.course_cannot_be_own_prerequisite import (
    CourseCannotBeOwnPrerequisiteError
)

from app.exceptions.course.course_no_fields_to_update import (
    CourseNoFieldsToUpdateError
)

from app.exceptions.course.course_has_dependencies import (
    CourseHasDependenciesError
)