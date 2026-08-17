from fastapi import FastAPI
from app.db.database import Base,engine
import app.models.user
from app.router.auth import auth
app = FastAPI(
    title="manager devconect"
)
Base.metadata.create_all(bind = engine)
@app.get("/")
def get_root():
    return {"message":"đang khởi chạy"}