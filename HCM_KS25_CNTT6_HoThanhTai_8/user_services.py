from database import Base, engine, get_db
from sqlalchemy.orm import Session
from models import TeamModel
from sqlalchemy.exc import SQLAlchemyError
from schemas import CreateTeamDTO

def get_all_team(db: Session):
    return db.query(TeamModel).all()

def get_team_id(db: Session, team_id: int):
    result = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if result is None:
        return {
            "status_code": "404",
            "message": "không tìm thấy"
        }
    return result
def create_team(db: Session, team: CreateTeamDTO):
    try:
        new_team = TeamModel(
            customer_name=team.customer_name,
            product_code=team.product_code,
            total_amount=team.total_amount,
            status=team.status
        )

        db.add(new_team)
        db.commit()
        db.refresh(new_team)

        return new_team
    except SQLAlchemyError:
        db.rollback()
        return {
            "status_code": "500",
            "message": "thêm thất bại"
        }
def delete_team(db: Session, team_id: int):
    result = db.query(TeamModel).filter(TeamModel.id == team_id).first()

    if result is None:
        return {
            "status_code": "404",
            "message": "không tìm thấy"
        }
    db.delete(result)
    db.commit()

    return {
        "message": "xóa thành công"
    }
def get_team_status(db: Session, status: str):
    result = db.query(TeamModel).filter(TeamModel.status == status).all()

    if len(result) == 0:
        return {
            "status_code": "404",
            "message": "không tìm thấy"
        }
    return result