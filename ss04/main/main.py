from fastapi import FastAPI,status,HTTPException
#kiểm soát và xử lí dữ liệu đầu vào
from pydantic import BaseModel,Field

app = FastAPI(
    title="Rikkei",
    description="MANAGER STUDENT",
    version="1.0.0"
)
#định nghĩa dữ liệu đầu vào
class StudentSchema(BaseModel):
    username: str = Field(...,min_length=2,max_length=100)
    password: str 
    age: int = Field(...,ge=18,le=90,description="phải lơn hơn 18 và nhỏ hơn 90")
    status: bool =True
#dữ liệu mẫu
student_dtb = [
    {"id":1,"username":"thanh tai","pass":"123","age":18},
    {"id":2,"username":"ronaldo","pass":"456","age":41,"status":False},
    {"id":3,"username":"messi","pass":"333","age":30},
    {"id":4,"username":"neyma.jr","pass":"444","age":19}
]
#tạo api để lấy ds sv
#decorater
@app.get("/students",tags=["students"])
def get_all_student():
    return {
        #mã trạng thái 200-300 tương đương xử lí thành công
        "status_code":200,
        "message":"lấy danh sách thành công",
        "data":student_dtb
    }
@app.post("/students",tags=["students"])
def add_students(student: StudentSchema):
    student_id = len(student_dtb)+1
    new_student = {
        "id":student_id,
        "username":student.username,
        "pass":student.password
    }
    student_dtb.append(new_student)
    return {
        "status_code":201,
        "message":"thêm sinh viên thành công",
        "data":new_student
    }
#tạo api để lấy sinh viên cụ thể 
#path parameter
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in student_dtb:
        if student_id == student.get("id"):
          return {
            "status_code":200,
            "message":"tìm kiếm thành công",
            "data": student
            }
    return {
        "message":"không tìm thấy"
    }
@app.get("/student",tags=["students"])
def get_students(
    keyword: str,
    limit: int,
    status:bool
):
    list_student = []
    for student in student_dtb:
        if keyword.lower() in student.get("username"):
            list_student.append(student)
    if not list_student:
        return {
            "message":"không tìm thấy"
        }
    rresult= list_student[:limit]
    return {
        "status_code":200,
        "message":"lấy danh sách thành công",
        "data":list_student
    }
#tạo api để xóa 1 sinh viên theo ID
@app.delete("/student/{student_id}",tags=["students"],status_code=200)
def del_student(student_id: int):
    # for student in student_dtb:
    #     if student.get("id")==student_id:
    #         student_dtb.remove(student)
    student_find = next((std for std in student_dtb if std.get("id")==student_id),None)
    if student_find is None:
            raise HTTPException(
            status_code= 404,
            detail="không tìm thấy"
        )
    student_dtb.remove(student_find)
    return {
        "status": 200,
        "message":"xóa sinh viên thành công",
        "data":student_find
    }
    # return{
    #     "message":"không tìm thấy sinh viên"
    # }
    
@app.patch("/student/{student_id}",tags=["students"])
def ud_student(
    student_id: int,
    student: StudentSchema
):
    for value in student_dtb:
        if value.get("id") == student_id:
            new_student = {
                "username":
            }
