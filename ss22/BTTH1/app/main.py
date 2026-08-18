from fastapi import FastAPI
from app.db.database import Base,engine
from app.models.models import User
import app.routers.auth as auth
from app.routers.auth import auth_all

app = FastAPI(
    title="Manager DevConnect"
)

Base.metadata.create_all(bind = engine)
app.include_router(auth_all)


@app.get("/")
def get_root():
    return{"message":"Sever dang khoi chay"}
