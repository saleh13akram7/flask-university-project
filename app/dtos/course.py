from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class CreateCourseDTO(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    name: str = Field(
        min_length=2,
        max_length=100
    )

    number_of_hours: int = Field(
        gt=0
    )

    pre_course_id: int | None = Field(
        default=None,
        gt=0
    )


class UpdateCourseDTO(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    number_of_hours: int | None = Field(
        default=None,
        gt=0
    )

    pre_course_id: int | None = Field(
        default=None,
        gt=0
    )


class CourseResponseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    number_of_hours: int
    pre_course_id: int | None