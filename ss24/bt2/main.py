from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FlashMove Logistics App",
    description="Hệ thống phân quyền RBAC và cấu hình CORS cho FlashMove"
)


# =========================
# CẤU HÌNH CORS
# =========================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "https://driver.flashmove.io",
        "https://hub.flashmove.io"
    ],

    allow_credentials=True,

    allow_methods=[
        "GET",
        "POST",
        "PATCH"
    ],

    allow_headers=[
        "Content-Type",
        "X-Role-Identity"
    ],
)


# =========================
# PHÂN QUYỀN CHO CÁC API
# =========================

ROLE_PERMISSIONS = {
    "/api/v1/orders/assign": [
        "DISPATCHER"
    ],

    "/api/v1/orders/status": [
        "DISPATCHER",
        "DRIVER"
    ],

    "/api/v1/orders/track": [
        "DISPATCHER",
        "DRIVER",
        "CUSTOMER_SUPPORT"
    ]
}


# =========================
# MIDDLEWARE PHÂN QUYỀN
# =========================

@app.middleware("http")
async def role_middleware(request: Request, call_next):

    # Lấy đường dẫn API đang được gọi
    path = request.url.path

    # Nếu API nằm trong danh sách cần phân quyền
    if path in ROLE_PERMISSIONS:

        # Lấy role từ Header
        user_role = request.headers.get("X-Role-Identity")

        # Lấy danh sách role được phép truy cập API
        allowed_roles = ROLE_PERMISSIONS[path]

        # Nếu role không hợp lệ thì chặn ngay
        if user_role not in allowed_roles:
            return JSONResponse(
                status_code=403,
                content={
                    "status": "Rejected",
                    "reason": "Unauthorized action for this role"
                }
            )

    # Nếu có quyền thì cho request đi tiếp
    response = await call_next(request)

    return response


# =========================
# API 1
# CHỈ DISPATCHER
# =========================

@app.post("/api/v1/orders/assign")
def assign_order():
    return {
        "message": "Gán đơn hàng cho tài xế thành công"
    }


# =========================
# API 2
# DISPATCHER + DRIVER
# =========================

@app.patch("/api/v1/orders/status")
def update_order_status():
    return {
        "message": "Cập nhật trạng thái đơn hàng thành công"
    }


# =========================
# API 3
# CẢ 3 ROLE
# =========================

@app.get("/api/v1/orders/track")
def track_order():
    return {
        "message": "Xem tiến trình đơn hàng thành công"
    }


@app.get("/")
def root():
    return {
        "message": "FlashMove Logistics API đang hoạt động"
    }