from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from models import Student, Workshop, Registration


# ==================================================
# STUDENT
# ==================================================

# Tạo sinh viên
def create_student(db: Session, student):

    check_code = db.query(Student).filter(
        Student.student_code == student.student_code
    ).first()

    if check_code:
        raise HTTPException(
            status_code=400,
            detail="Student code already exists"
        )

    check_email = db.query(Student).filter(
        Student.email == student.email
    ).first()

    if check_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_student = Student(
        student_code=student.student_code,
        full_name=student.full_name,
        email=student.email,
        status=student.status
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# Danh sách sinh viên
def get_students(db: Session):

    return db.query(Student).all()


# ==================================================
# WORKSHOP
# ==================================================

# Tạo workshop
def create_workshop(db: Session, workshop):

    new_workshop = Workshop(
        title=workshop.title,
        description=workshop.description,
        maximum_participants=workshop.maximum_participants,
        status=workshop.status,
        start_time=workshop.start_time
    )

    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)

    return new_workshop


# Danh sách workshop
def get_workshops(db: Session):

    return db.query(Workshop).all()


# Chi tiết workshop
def get_workshop_by_id(db: Session, workshop_id: int):

    workshop = db.query(Workshop).filter(
        Workshop.id == workshop_id
    ).first()

    if not workshop:
        raise HTTPException(
            status_code=404,
            detail="Workshop not found"
        )

    return workshop


# ==================================================
# REGISTRATION
# ==================================================

# Đăng ký workshop
def create_registration(db: Session, registration):

    # Kiểm tra sinh viên
    student = db.query(Student).filter(
        Student.id == registration.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Kiểm tra workshop
    workshop = db.query(Workshop).filter(
        Workshop.id == registration.workshop_id
    ).first()

    if not workshop:
        raise HTTPException(
            status_code=404,
            detail="Workshop not found"
        )

    # Sinh viên phải ACTIVE
    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Student is inactive"
        )

    # Workshop phải OPEN
    if workshop.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Workshop is closed"
        )

    # Kiểm tra đăng ký trùng
    check_registration = db.query(Registration).filter(
        Registration.student_id == registration.student_id,
        Registration.workshop_id == registration.workshop_id,
        Registration.status == "REGISTERED"
    ).first()

    if check_registration:
        raise HTTPException(
            status_code=400,
            detail="Student already registered"
        )

    # Kiểm tra workshop đã đủ người
    total = db.query(Registration).filter(
        Registration.workshop_id == registration.workshop_id,
        Registration.status == "REGISTERED"
    ).count()

    if total >= workshop.maximum_participants:
        raise HTTPException(
            status_code=400,
            detail="Workshop is full"
        )

    new_registration = Registration(
        student_id=registration.student_id,
        workshop_id=registration.workshop_id,
        registered_at=datetime.utcnow(),
        status="REGISTERED"
    )

    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)

    return new_registration


# ==================================================
# WORKSHOP CỦA MỘT SINH VIÊN
# ==================================================

def get_student_workshops(db: Session, student_id: int):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    workshops = []

    for registration in student.registrations:

        if registration.status == "REGISTERED":

            workshops.append({
                "id": registration.workshop.id,
                "title": registration.workshop.title
            })

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "workshops": workshops
    }


# ==================================================
# DANH SÁCH SINH VIÊN CỦA WORKSHOP
# ==================================================

def get_workshop_students(db: Session, workshop_id: int):

    workshop = db.query(Workshop).filter(
        Workshop.id == workshop_id
    ).first()

    if not workshop:
        raise HTTPException(
            status_code=404,
            detail="Workshop not found"
        )

    students = []

    for registration in workshop.registrations:

        if registration.status == "REGISTERED":

            students.append({
                "id": registration.student.id,
                "student_code": registration.student.student_code,
                "full_name": registration.student.full_name
            })

    return {
        "workshop_id": workshop.id,
        "title": workshop.title,
        "students": students
    }


# ==================================================
# HỦY ĐĂNG KÝ
# ==================================================

def cancel_registration(db: Session, registration_id: int):

    registration = db.query(Registration).filter(
        Registration.id == registration_id
    ).first()

    if not registration:
        raise HTTPException(
            status_code=404,
            detail="Registration not found"
        )

    registration.status = "CANCELLED"

    db.commit()
    db.refresh(registration)

    return {
        "message": "Registration cancelled successfully"
    }