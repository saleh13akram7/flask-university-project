from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


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