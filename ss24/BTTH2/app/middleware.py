from fastapi import Request
from fastapi.responses import JSONResponse


# Quyền của từng API
ROLE_PERMISSIONS = {
    "/api/v1/orders/assign": ["DISPATCHER"],
    "/api/v1/orders/status": ["DISPATCHER", "DRIVER"],
    "/api/v1/orders/track": ["DISPATCHER", "DRIVER", "CUSTOMER_SUPPORT"],
}


async def authorization_middleware(request: Request, call_next):
    path = request.url.path

    # Kiểm tra các API cần phân quyền
    if path in ROLE_PERMISSIONS:

        # Lấy role từ Header
        user_role = request.headers.get("X-Role-Identity")

        # Role không có quyền truy cập
        if user_role not in ROLE_PERMISSIONS[path]:
            return JSONResponse(
                status_code=403,
                content={
                    "status": "Rejected",
                    "reason": "Unauthorized action for this role"
                }
            )

    # Role hợp lệ -> cho request đi tiếp
    response = await call_next(request)

    return response