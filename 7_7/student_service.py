from sqlalchemy.orm import Session
from model import StudentRequestDTO,StudentModel
def create_student(db: Session,student: StudentRequestDTO):
    try:
        new_student = StudentModel(
            id= student.id,
            full_name= student.full_name,
            email= student.email
        )
    db.add(new_student)
    db.commit()
    db.refresh()
    return{
        "status_code":201,
        "message":"thêm thành công"
    }
