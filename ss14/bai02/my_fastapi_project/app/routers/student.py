from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.student import StudentCreate, StudentOut, StudentUpdate
from ..services.student import (
    get_students,
    get_student,
    create_student,
    update_student,
    delete_student,
)

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return get_students(db)


@router.get("/{student_id}", response_model=StudentOut)
def read_student(student_id: int, db: Session = Depends(get_db)):
    s = get_student(db, student_id)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return s


@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student_endpoint(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, student)


@router.put("/{student_id}", response_model=StudentOut)
def update_student_endpoint(student_id: int, updates: StudentUpdate, db: Session = Depends(get_db)):
    db_student = get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return update_student(db, db_student, updates)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    db_student = get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    delete_student(db, db_student)
    return
