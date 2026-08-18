from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import authorization_middleware


app = FastAPI()


# =========================
# CẤU HÌNH CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://driver.flashmove.io",
        "https://hub.flashmove.io",
    ],
    allow_methods=[
        "GET",
        "POST",
        "PATCH",
    ],
    allow_headers=[
        "Content-Type",
        "X-Role-Identity",
    ],
)


# =========================
# CUSTOM MIDDLEWARE
# =========================

app.middleware("http")(authorization_middleware)


# =========================
# API ENDPOINTS
# =========================


# Chỉ DISPATCHER được gán đơn hàng
@app.post("/api/v1/orders/assign")
def assign_order():
    return {
        "status": "Success",
        "message": "Order assigned successfully"
    }


# DISPATCHER và DRIVER được cập nhật trạng thái
@app.patch("/api/v1/orders/status")
def update_order_status():
    return {
        "status": "Success",
        "message": "Order status updated successfully"
    }


# Cả 3 role được xem tiến trình đơn hàng
@app.get("/api/v1/orders/track")
def track_order():
    return {
        "status": "Success",
        "message": "Order tracking information"
    }