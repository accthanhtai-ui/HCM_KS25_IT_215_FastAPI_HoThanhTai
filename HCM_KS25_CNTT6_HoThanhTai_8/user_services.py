from database import Base,engine,get_db
from sqlalchemy.orm import Session
from models import TeamModel
from sqlalchemy.exc import SQLAlchemyError

def get_all_team(db:Session):
    return db.query(TeamModel).all()
##tìm theo id
def get_team_id(db:Session,team_id:int):
    result = db.query(TeamModel).filter(TeamModel.id==team_id).first()
    if result is None :
        return {
            "status_code":"404",
            "message": "không tìm thấy"
        }
    return result

