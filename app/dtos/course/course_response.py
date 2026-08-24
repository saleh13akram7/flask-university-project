from pydantic import (
    BaseModel,
    ConfigDict
)


class CourseResponseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    number_of_hours: int
    pre_course_id: int | None