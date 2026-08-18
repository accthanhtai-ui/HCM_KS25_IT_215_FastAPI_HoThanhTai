from datetime import datetime, timezone

from fastapi import (
    FastAPI,
    Depends,
    Request,
    HTTPException,
    Query
)

from fastapi.exceptions import RequestValidationError

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from database import (
    Base,
    engine,
    get_db
)

from schemas import (
    StudentCreateDTO,
    StudentUpdateDTO
)

import models
import services


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Quản Lý Sinh Viên Theo Lớp Học",
    version="1.0.0"
)


def get_timestamp():
    return datetime.now(
        timezone.utc
    ).isoformat()


def success_response(
    status_code: int,
    message: str,
    data,
    path: str
):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": None,
        "timestamp": get_timestamp(),
        "path": path
    }


def student_to_dict(student):
    return {
        "id": student.id,
        "studentCode": student.student_code,
        "fullName": student.full_name,
        "email": student.email,
        "class": {
            "id": student.classroom.id,
            "classCode": student.classroom.class_code,
            "className": student.classroom.class_name
        }
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        errors.append({
            "field": error["loc"][-1],
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "statusCode": 422,
            "message": "Dữ liệu đầu vào không hợp lệ!",
            "data": None,
            "error": errors,
            "timestamp": get_timestamp(),
            "path": request.url.path
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    if isinstance(exc.detail, dict):
        message = exc.detail.get(
            "message",
            "Yêu cầu thất bại!"
        )

        error = exc.detail.get(
            "error"
        )

    else:
        message = str(exc.detail)
        error = None

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": message,
            "data": None,
            "error": error,
            "timestamp": get_timestamp(),
            "path": request.url.path
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "message": "Lỗi hệ thống!",
            "data": None,
            "error": "INTERNAL_SERVER_ERROR",
            "timestamp": get_timestamp(),
            "path": request.url.path
        }
    )


@app.get("/students")
def get_students(
    request: Request,
    keyword: str | None = Query(
        default=None
    ),
    class_id: int | None = Query(
        default=None,
        ge=1
    ),
    page: int = Query(
        default=1,
        ge=1
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    db: Session = Depends(get_db)
):
    result = services.get_all_students(
        db,
        keyword,
        class_id,
        page,
        limit
    )

    items = []

    for student in result["items"]:
        items.append(
            student_to_dict(student)
        )

    data = {
        "total": result["total"],
        "items": items
    }

    return success_response(
        200,
        "Lấy danh sách sinh viên thành công!",
        data,
        request.url.path
    )


@app.get("/students/{student_id}")
def get_student_detail(
    student_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    student = services.get_student_by_id(
        db,
        student_id
    )

    data = student_to_dict(
        student
    )

    return success_response(
        200,
        "Lấy chi tiết sinh viên thành công!",
        data,
        request.url.path
    )


@app.post(
    "/students",
    status_code=201
)
def create_student(
    data: StudentCreateDTO,
    request: Request,
    db: Session = Depends(get_db)
):
    student = services.create_student(
        db,
        data
    )

    result = student_to_dict(
        student
    )

    return JSONResponse(
        status_code=201,
        content=success_response(
            201,
            "Thêm mới sinh viên thành công!",
            result,
            request.url.path
        )
    )


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    data: StudentUpdateDTO,
    request: Request,
    db: Session = Depends(get_db)
):
    student = services.update_student(
        db,
        student_id,
        data
    )

    result = student_to_dict(
        student
    )

    return success_response(
        200,
        "Cập nhật sinh viên thành công!",
        result,
        request.url.path
    )