from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime

app = FastAPI(title="Elearning Course API")

courses_db = [
    {
        "id": 1,
        "course_name": "FastAPI Masterclass",
        "duration_hours": 32,
        "price": 1500000,
        "status": "active",
        "created_at": "2026-07-01T02:00:00Z"
    },
    {
        "id": 2,
        "course_name": "NextJS Next-Level",
        "duration_hours": 45,
        "price": 1800000,
        "status": "active",
        "created_at": "2026-07-01T03:15:00Z"
    }
]


class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Any
    error: Any
    timestamp: str
    path: str


class CourseCreate(BaseModel):
    course_name: str = Field(..., min_length=5)
    duration_hours: int = Field(..., gt=0)
    price: int = Field(..., ge=0)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    if exc.status_code == 400:
        message = "Lỗi: Tên khóa học này đã tồn tại trong danh mục đào tạo!"
    elif exc.status_code == 404:
        message = "Lỗi: Không tìm thấy mã khóa học yêu cầu để xóa!"
    else:
        message = "Đã xảy ra lỗi!"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": message,
            "data": None,
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": request.url.path
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "statusCode": 422,
            "message": "Dữ liệu đầu vào không hợp lệ!",
            "data": None,
            "error": exc.errors(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": request.url.path
        }
    )


@app.get("/courses")
def get_courses(request: Request):
    return APIResponse(
        statusCode=200,
        message="Lấy danh sách khóa học thành công!",
        data=courses_db,
        error=None,
        timestamp=datetime.utcnow().isoformat() + "Z",
        path=request.url.path
    )


@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, request: Request):

    for item in courses_db:
        if item["course_name"] == course.course_name:
            raise HTTPException(
                status_code=400,
                detail="ERR-EDU-01: Course name duplicates an existing record in memory array."
            )

    new_course = {
        "id": len(courses_db) + 1,
        "course_name": course.course_name,
        "duration_hours": course.duration_hours,
        "price": course.price,
        "status": "active",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    courses_db.append(new_course)

    return APIResponse(
        statusCode=201,
        message="Tạo mới khóa học thành công!",
        data=new_course,
        error=None,
        timestamp=datetime.utcnow().isoformat() + "Z",
        path=request.url.path
    )


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, request: Request):

    for item in courses_db:
        if item["id"] == course_id:
            courses_db.remove(item)

            return APIResponse(
                statusCode=200,
                message="Xóa khóa học thành công!",
                data=None,
                error=None,
                timestamp=datetime.utcnow().isoformat() + "Z",
                path=request.url.path
            )

    raise HTTPException(
        status_code=404,
        detail="ERR-EDU-02: Target course ID can not be found."
    )