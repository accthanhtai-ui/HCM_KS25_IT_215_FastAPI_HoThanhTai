from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from schemas import (
    StudentCreate,
    StudentResponse,
    WorkshopCreate,
    WorkshopResponse,
    RegistrationCreate,
    RegistrationResponse
)

from crud import (
    create_student,
    get_students,
    create_workshop,
    get_workshops,
    get_workshop_by_id,
    create_registration,
    get_student_workshops,
    get_workshop_students,
    cancel_registration
)

# Import model để SQLAlchemy tạo bảng
from models import Student, Workshop, Registration

# Tạo bảng
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Workshop Registration API",
    version="1.0.0"
)


# ==========================================================
# HOME
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "Workshop Registration API"
    }


# ==========================================================
# STUDENT
# ==========================================================

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return create_student(db, student)


@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def students(
    db: Session = Depends(get_db)
):
    return get_students(db)


# ==========================================================
# WORKSHOP
# ==========================================================

@app.post(
    "/workshops",
    response_model=WorkshopResponse,
    status_code=status.HTTP_201_CREATED
)
def add_workshop(
    workshop: WorkshopCreate,
    db: Session = Depends(get_db)
):
    return create_workshop(db, workshop)


@app.get(
    "/workshops",
    response_model=list[WorkshopResponse]
)
def workshops(
    db: Session = Depends(get_db)
):
    return get_workshops(db)


@app.get(
    "/workshops/{workshop_id}",
    response_model=WorkshopResponse
)
def workshop_detail(
    workshop_id: int,
    db: Session = Depends(get_db)
):
    return get_workshop_by_id(db, workshop_id)


# ==========================================================
# REGISTRATION
# ==========================================================

@app.post(
    "/registrations",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def register_workshop(
    registration: RegistrationCreate,
    db: Session = Depends(get_db)
):
    return create_registration(db, registration)


@app.get("/students/{student_id}/workshops")
def student_workshops(
    student_id: int,
    db: Session = Depends(get_db)
):
    return get_student_workshops(db, student_id)


@app.get("/workshops/{workshop_id}/students")
def workshop_students(
    workshop_id: int,
    db: Session = Depends(get_db)
):
    return get_workshop_students(db, workshop_id)


@app.delete("/registrations/{registration_id}")
def delete_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):
    return cancel_registration(db, registration_id)