from pydantic import (
    BaseModel,
    ConfigDict
)


class StudentResponseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str | None = None
    phone_number: str | None = None
    email_address: str | None = None
    major_id: int | None = None