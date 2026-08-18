from fastapi import FastAPI

from app.routers.medical import medical_router


app = FastAPI(
    title="MedCare E-Prescription API"
)


app.include_router(medical_router)


@app.get("/")
def root():
    return {
        "message": "MedCare API đang chạy"
    }