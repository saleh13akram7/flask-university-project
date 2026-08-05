from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateStudentDTO(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    name: str = Field(
        min_length=2,
        max_length=100
    )

    phone_number: str = Field(
        min_length=7,
        max_length=20
    )

    email_address: EmailStr

    major_id: int = Field(
        gt=0
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


class StudentResponseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    phone_number: str
    email_address: str
    major_id: int