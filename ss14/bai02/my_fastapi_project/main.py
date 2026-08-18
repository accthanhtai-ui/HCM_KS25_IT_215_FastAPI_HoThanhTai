# Package-aware imports
from fastapi import FastAPI
from .app.routers import student as student_router
from .app.database import Base, engine

# Create database tables (runs at startup)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")

app.include_router(student_router.router)
