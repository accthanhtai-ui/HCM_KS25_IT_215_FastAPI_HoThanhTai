from fastapi import FastAPI, HTTPException,requests,status
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, timezone
app = FastAPI(
    title="Manager Student"
)
class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any]
    error: Optional[Any]
    timestamp: str
    path: str

# dữ liệu trả về thành công
def success_response(statusCode: int, message: str, data:Any,request: Request):
    return APIResponse(
        statusCode= statusCode,
        message= message,
        data= data,
        error = None,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path = request.url.path
    )

# định nghĩa dữ liệu client gửi lên
class StudeRequestDTO(BaseModel):
    username: str
    emai : str
    password : str
# định nghĩa dữ liệu trả về cho client
class StudentResponseDTO(BaseModel):
    username  : str
    email :str
student_database = [
    {"id": 1, "username": "Trọng Nguyên", "email": "Trongnguyen@gmail.com", "password": "12543"},
    {"id": 2, "username": "Thanh Tài", "email": "Thanhtai@gmail.com", "password": "18763"},
    {"id": 3, "username": "Ánh Hồng", "email": "anhhong@gmail.com", "password": "1234"},
    {"id": 4, "username": "Kim Ngân", "email": "kimngan@gmail.com", "password": "345"},
]
# tạo api thêm sinh viên
@app.post("/students/", response_model=StudentResponseDTO ,)
def create_student(student: StudeRequestDTO):
    new_student = {
        "id": len(student_database)+1,
        "username": student.username,
        "email": student.email,
        "password": student.password
    }
    student_database.append(new_student)

    return success_response(s)
# API lấy sinh viên theo id
@app.get("/students/{student_id}", tags=["students"], response_model= StudentResponseDTO)
def get_student(student_id: int):
    for student in student_database:
        if student.get("id") == student_id:
            return student
            # return {
            #     "status": "200",
            #     "message": "lấy thông tin thành công",
            #     "data": student
            # }
    raise HTTPException(status_code=404,detail="Student not found")
        
