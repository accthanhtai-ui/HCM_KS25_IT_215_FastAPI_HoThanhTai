from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()


# Chỉ cho phép 2 Frontend được kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


TOKENS = {
    "admin-token": {
        "username": "admin01",
        "role": "admin",
        "is_active": True,
    },
    "user-token": {
        "username": "student01",
        "role": "user",
        "is_active": True,
    },
    "locked-token": {
        "username": "locked01",
        "role": "user",
        "is_active": False,
    },
}


# Middleware kiểm tra Authentication
@app.middleware("http")
async def authentication_middleware(request, call_next):

    # Các endpoint được phép truy cập công khai
    public_paths = [
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
    ]

    # Không yêu cầu Authorization cho endpoint công khai
    if request.url.path in public_paths:
        response = await call_next(request)

        response.headers["X-System-Name"] = (
            "Learning Management System"
        )

        return response

    # OPTIONS là CORS preflight
    # Không được yêu cầu JWT
    if request.method == "OPTIONS":
        response = await call_next(request)

        response.headers["X-System-Name"] = (
            "Learning Management System"
        )

        return response

    # Các API còn lại phải có Authorization
    if "authorization" not in request.headers:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Authorization header is required"
            },
        )

    response = await call_next(request)

    response.headers["X-System-Name"] = (
        "Learning Management System"
    )

    return response


# Lấy người dùng hiện tại
def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    user = TOKENS.get(token)

    # Token không hợp lệ
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    # Tài khoản bị khóa
    if not user["is_active"]:
        raise HTTPException(
            status_code=403,
            detail="User is inactive",
        )

    return user


# Kiểm tra quyền Admin
def require_admin(
    current_user: dict = Depends(get_current_user)
):
    # Chỉ Admin mới được phép
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin permission required",
        )

    return current_user


# API kiểm tra trạng thái hệ thống
# Không cần đăng nhập
@app.get("/health")
def health_check():
    return {
        "status": "UP"
    }


# User và Admin đều được xem danh sách khóa học
@app.get("/courses")
def get_courses(
    current_user: dict = Depends(get_current_user)
):
    return {
        "items": [
            {
                "id": 1,
                "name": "FastAPI Basic"
            },
            {
                "id": 2,
                "name": "FastAPI Security"
            },
        ]
    }


# Chỉ Admin được xóa khóa học
@app.delete("/admin/courses/{course_id}")
def delete_course(
    course_id: int,
    current_user: dict = Depends(require_admin),
):
    return {
        "message": f"Course {course_id} has been deleted",
        "deleted_by": current_user["username"],
    }