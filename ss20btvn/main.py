from datetime import datetime, timezone

from fastapi import (
    FastAPI,
    Depends,
    Request,
    HTTPException,
    Query
)

from fastapi.responses import JSONResponse

from fastapi.exceptions import RequestValidationError

from sqlalchemy.orm import Session

from database import (
    Base,
    engine,
    get_db
)

from schemas import (
    StudentCreateDTO,
    StudentUpdateDTO,
    StudentResponse
)

import models

import services


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="API Quản Lý Sinh Viên Theo Lớp Học",
    version="1.0.0"
)


def get_timestamp():
    return datetime.now(
        timezone.utc
    ).isoformat()


def success_response(
    status_code,
    message,
    data,
    path
):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": None,
        "timestamp": get_timestamp(),
        "path": path
    }


@app.exception_handler(
    RequestValidationError
)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "statusCode": 422,
            "message": "Dữ liệu đầu vào không hợp lệ",
            "data": None,
            "error": exc.errors(),
            "timestamp": get_timestamp(),
            "path": request.url.path
        }
    )


@app.exception_handler(
    HTTPException
)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    if isinstance(
        exc.detail,
        dict
    ):
        message = exc.detail.get(
            "message"
        )

        error = exc.detail.get(
            "error"
        )

    else:
        message = str(
            exc.detail
        )

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


@app.exception_handler(
    Exception
)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "message": "Lỗi hệ thống",
            "data": None,
            "error": "INTERNAL_SERVER_ERROR",
            "timestamp": get_timestamp(),
            "path": request.url.path
        }
    )


@app.get(
    "/students"
)
def get_students(
    request: Request,

    keyword: str = Query(
        default=None
    ),

    class_id: int = Query(
        default=None,
        ge=1
    ),

    db: Session = Depends(
        get_db
    )
):
    students = services.get_all_students(
        db,
        keyword,
        class_id
    )

    data = []

    for student in students:

        student_data = StudentResponse.model_validate(
            student
        ).model_dump()

        data.append(
            student_data
        )

    return success_response(
        200,
        "Lấy danh sách sinh viên thành công",
        data,
        request.url.path
    )


@app.get(
    "/students/{student_id}"
)
def get_student_detail(
    student_id: int,

    request: Request,

    db: Session = Depends(
        get_db
    )
):
    student = services.get_student_by_id(
        db,
        student_id
    )

    data = StudentResponse.model_validate(
        student
    ).model_dump()

    return success_response(
        200,
        "Lấy chi tiết sinh viên thành công",
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

    db: Session = Depends(
        get_db
    )
):
    student = services.create_student(
        db,
        data
    )

    result = StudentResponse.model_validate(
        student
    ).model_dump()

    return JSONResponse(
        status_code=201,
        content=success_response(
            201,
            "Thêm sinh viên thành công",
            result,
            request.url.path
        )
    )


@app.put(
    "/students/{student_id}"
)
def update_student(
    student_id: int,

    data: StudentUpdateDTO,

    request: Request,

    db: Session = Depends(
        get_db
    )
):
    student = services.update_student(
        db,
        student_id,
        data
    )

    result = StudentResponse.model_validate(
        student
    ).model_dump()

    return success_response(
        200,
        "Cập nhật sinh viên thành công",
        result,
        request.url.path
    )