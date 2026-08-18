from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Student,Course,Enrollment


def create_enrollment(db:Session,data):

    student=db.query(Student).filter(Student.id==data.student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course=db.query(Course).filter(Course.id==data.course_id).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    if student.status!="ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Student inactive"
        )

    if course.status!="OPEN":
        raise HTTPException(
            status_code=400,
            detail="Course closed"
        )

    check=db.query(Enrollment).filter(
        Enrollment.student_id==data.student_id,
        Enrollment.course_id==data.course_id
    ).first()

    if check:
        raise HTTPException(
            status_code=400,
            detail="Already enrolled"
        )

    total=db.query(Enrollment).filter(
        Enrollment.course_id==data.course_id
    ).count()

    if total>=course.max_students:
        raise HTTPException(
            status_code=400,
            detail="Course is full"
        )

    enroll=Enrollment(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(enroll)
    db.commit()
    db.refresh(enroll)

    return enroll


def get_student_courses(db:Session,student_id:int):

    student=db.query(Student).filter(
        Student.id==student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    result=[]

    for enroll in student.enrollments:

        result.append({

            "id":enroll.course.id,

            "name":enroll.course.name

        })

    return {

        "student_id":student.id,

        "full_name":student.full_name,

        "courses":result

    }