from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


class UpdateStudentDTO(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    phone_number: str | None = Field(
        default=None,
        min_length=7,
        max_length=20
    )

    email_address: EmailStr | None = None

    major_id: int | None = Field(
        default=None,
        gt=0
    )