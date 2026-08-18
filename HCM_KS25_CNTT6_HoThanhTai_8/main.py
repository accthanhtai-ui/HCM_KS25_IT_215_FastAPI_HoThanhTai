from fastapi import FastAPI, status, Depends
from database import Base, engine, get_db
from sqlalchemy.orm import Session
from schemas import CreateTeamDTO
import user_services

app = FastAPI(
    title="Customer Manergement"
)

Base.metadata.create_all(engine)

@app.get("/")
def get_root():
    return "kết nối thành công"

@app.get("/order", tags=["order"], status_code=status.HTTP_200_OK)
def get_all_team(db: Session = Depends(get_db)):
    team_data = user_services.get_all_team(db)
    return {
        "message": "lấy thông tin thành công",
        "data": team_data
    }

@app.get("/order/{team_id}", tags=["order"], status_code=status.HTTP_200_OK)
def search_id(team_id: int, db: Session = Depends(get_db)):
    team_data = user_services.get_team_id(db, team_id)
    return {
        "message": "tìm kiếm theo id thành công",
        "data": team_data
    }

@app.post("/order", tags=["order"], status_code=status.HTTP_201_CREATED)
def create_team(team: CreateTeamDTO, db: Session = Depends(get_db)):
    team_data = user_services.create_team(db, team)
    return {
        "message": "thêm thành công",
        "data": team_data
    }

@app.delete("/order/{team_id}", tags=["order"], status_code=status.HTTP_200_OK)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team_data = user_services.delete_team(db, team_id)
    return {
        "message": "xóa thành công",
        "data": team_data
    }

@app.get("/order/status/{status}", tags=["order"], status_code=status.HTTP_200_OK)
def search_status(status: str, db: Session = Depends(get_db)):
    team_data = user_services.get_team_status(db, status)
    return {
        "message": "tìm kiếm theo trạng thái thành công",
        "data": team_data
    }