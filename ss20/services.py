from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from models import (
    StudentModel,
    ClassModel
)

from schemas import (
    StudentCreateDTO,
    StudentUpdateDTO
)


def get_all_students(
    db: Session,
    keyword: str | None = None,
    class_id: int | None = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(StudentModel)

    if keyword:
        query = query.filter(
            or_(
                StudentModel.full_name.contains(keyword),
                StudentModel.student_code.contains(keyword),
                StudentModel.email.contains(keyword)
            )
        )

    if class_id:
        query = query.filter(
            StudentModel.class_id == class_id
        )

    total = query.count()

    students = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total": total,
        "items": students
    }


def get_student_by_id(
    db: Session,
    student_id: int
):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Không tìm thấy sinh viên!",
                "error": "ERR-STUDENT-01"
            }
        )

    return student


def check_class(
    db: Session,
    class_id: int
):
    classroom = db.query(ClassModel).filter(
        ClassModel.id == class_id
    ).first()

    if classroom is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Không tìm thấy lớp học!",
                "error": "ERR-CLASS-01"
            }
        )

    if classroom.status != "active":
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Lớp học không hoạt động!",
                "error": "ERR-CLASS-02"
            }
        )

    student_count = db.query(StudentModel).filter(
        StudentModel.class_id == class_id
    ).count()

    if student_count >= classroom.max_students:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Lớp học đã đầy!",
                "error": "ERR-CLASS-03"
            }
        )

    return classroom


def check_student_code(
    db: Session,
    student_code: str,
    student_id: int | None = None
):
    query = db.query(StudentModel).filter(
        StudentModel.student_code == student_code
    )

    if student_id is not None:
        query = query.filter(
            StudentModel.id != student_id
        )

    student = query.first()

    if student:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Mã sinh viên đã tồn tại!",
                "error": "ERR-STUDENT-02"
            }
        )


def check_email(
    db: Session,
    email: str,
    student_id: int | None = None
):
    query = db.query(StudentModel).filter(
        StudentModel.email == email
    )

    if student_id is not None:
        query = query.filter(
            StudentModel.id != student_id
        )

    student = query.first()

    if student:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Email đã tồn tại!",
                "error": "ERR-STUDENT-03"
            }
        )


def create_student(
    db: Session,
    data: StudentCreateDTO
):
    check_class(
        db,
        data.classId
    )

    check_student_code(
        db,
        data.studentCode
    )

    check_email(
        db,
        str(data.email)
    )

    new_student = StudentModel(
        student_code=data.studentCode,
        full_name=data.fullName,
        email=str(data.email),
        class_id=data.classId
    )

    try:
        db.add(new_student)

        db.commit()

        db.refresh(new_student)

        return new_student

    except Exception:
        db.rollback()

        raise


def update_student(
    db: Session,
    student_id: int,
    data: StudentUpdateDTO
):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Không tìm thấy sinh viên!",
                "error": "ERR-STUDENT-01"
            }
        )

    check_student_code(
        db,
        data.studentCode,
        student_id
    )

    check_email(
        db,
        str(data.email),
        student_id
    )

    if student.class_id != data.classId:
        check_class(
            db,
            data.classId
        )

    student.student_code = data.studentCode

    student.full_name = data.fullName

    student.email = str(data.email)

    student.class_id = data.classId

    try:
        db.commit()

        db.refresh(student)

        return student

    except Exception:
        db.rollback()

        raise