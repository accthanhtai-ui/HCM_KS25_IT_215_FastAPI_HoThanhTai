from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional,Any
from datetime import datetime,timezone

app = FastAPI(title="Elearning Course")

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

#cái này là khuông mẫu trả về
class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[any] = None #dùng giá trị mặc định là dấu bằng
    error: Optional[any] = None
    timestamp: str
    path: str
#tạo hàm trả về khi thành công
def success_response(statusCode: int , message: str,data: Any,req: Request):
    return APIResponse(
        statusCode=statusCode,
        message=message,
        data=data,
        error =None,
        timestamp=datetime.now(timezone.utc).isoformat,
        path=req.url.path
    )
@app.get("/courses",tags=["courses"])
def get_courses(req: Request):
    return success_response(200,"lấy dữ liệu thành công",courses_db,req)