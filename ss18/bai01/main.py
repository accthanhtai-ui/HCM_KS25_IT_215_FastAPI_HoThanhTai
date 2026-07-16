from fastapi import FastAPI,Depends,status
from sqlalchemy.orm import Session

from database import Base,engine,get_db
from schemas import EnrollmentCreate,EnrollmentResponse
from curd import create_enrollment,get_student_courses

Base.metadata.create_all(bind=engine)

app=FastAPI()


@app.post(
    "/enrollments",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll(
    data:EnrollmentCreate,
    db:Session=Depends(get_db)
):
    return create_enrollment(db,data)


@app.get("/students/{student_id}/courses")
def student_courses(
    student_id:int,
    db:Session=Depends(get_db)
):
    return get_student_courses(db,student_id)