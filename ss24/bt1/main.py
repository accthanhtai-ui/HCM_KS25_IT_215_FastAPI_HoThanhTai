from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MegaMart ERP",
    description="Hệ thống ERP với phân quyền RBAC và bảo mật CORS"
)


# =========================
# CẤU HÌNH CORS
# =========================

app.add_middleware(
    CORSMiddleware,

    # Chỉ cho phép Frontend chính thức của MegaMart
    allow_origins=[
        "https://internal.megamart.com"
    ],

    # Cho phép gửi thông tin xác thực nếu cần
    allow_credentials=True,

    # Theo đề chỉ cho GET và POST
    allow_methods=[
        "GET",
        "POST"
    ],

    # Theo đề chỉ cho phép 2 Header này
    allow_headers=[
        "Content-Type",
        "X-User-Role"
    ],
)


# =========================
# DANH SÁCH PHÂN QUYỀN
# =========================

ROLE_PERMISSIONS = {
    "/api/v1/salary/modify": ["ADMIN", "HR"],

    "/api/v1/system/settings": ["ADMIN"],

    "/api/v1/profile": ["ADMIN", "HR", "STAFF"]
}


# =========================
# MIDDLEWARE PHÂN QUYỀN
# =========================

@app.middleware("http")
async def role_middleware(request: Request, call_next):

    # Lấy đường dẫn API mà người dùng đang gọi
    path = request.url.path

    # Kiểm tra API có nằm trong danh sách cần bảo vệ không
    if path in ROLE_PERMISSIONS:

        # Lấy role từ Header X-User-Role
        user_role = request.headers.get("X-User-Role")

        # Lấy danh sách role được phép truy cập API
        allowed_roles = ROLE_PERMISSIONS[path]

        # Kiểm tra quyền
        if user_role not in allowed_roles:
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Permission Denied"
                }
            )

    # Có quyền thì cho request đi tiếp vào API
    response = await call_next(request)

    return response


# =========================
# API 1 - SALARY
# ADMIN + HR
# =========================

@app.get("/api/v1/salary/modify")
def modify_salary():
    return {
        "message": "Truy cập chức năng quản lý bảng lương thành công"
    }


# =========================
# API 2 - SYSTEM SETTINGS
# CHỈ ADMIN
# =========================

@app.get("/api/v1/system/settings")
def system_settings():
    return {
        "message": "Truy cập cài đặt hệ thống thành công"
    }


# =========================
# API 3 - PROFILE
# ADMIN + HR + STAFF
# =========================

@app.get("/api/v1/profile")
def profile():
    return {
        "message": "Truy cập thông tin cá nhân thành công"
    }


# =========================
# API ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "MegaMart ERP API đang hoạt động"
    }