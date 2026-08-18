from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


class ClassResponse(BaseModel):
    id: int

    classCode: str = Field(
        validation_alias="class_code"
    )

    className: str = Field(
        validation_alias="class_name"
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class StudentCreateDTO(BaseModel):
    studentCode: str = Field(
        min_length=3,
        max_length=20
    )

    fullName: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    classId: int = Field(
        ge=1
    )


class StudentUpdateDTO(BaseModel):
    studentCode: str = Field(
        min_length=3,
        max_length=20
    )

    fullName: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    classId: int = Field(
        ge=1
    )


class StudentResponse(BaseModel):
    id: int

    studentCode: str

    fullName: str

    email: str

    classInfo: ClassResponse = Field(
        serialization_alias="class"
    )

    model_config = ConfigDict(
        populate_by_name=True
    )


class APIResponse(BaseModel):
    statusCode: int

    message: str

    data: Any = None

    error: Any = None

    timestamp: str

    path: str