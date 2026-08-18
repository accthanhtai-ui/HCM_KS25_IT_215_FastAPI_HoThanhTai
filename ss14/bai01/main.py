from fastapi import FastAPI
from database import Base, engine
from sqlalchemy.exc import OperationalError
from routers import router

try:
    Base.metadata.create_all(bind=engine)
except OperationalError:
    print("Warning: database not available — skipping metadata.create_all()")

app = FastAPI(
    title="Product Management API"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Product Management API"
    }