from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from Database import get_db, Base, engine
from sqlalchemy import text
from models import UserModel
from user_services import create_user, get_user, update_user
from schemas import UserRequestDTo

app = FastAPI(
    title="Manager Users"
)
Base.metadata.create_all(bind = engine)
@app.get("/test-connection")
def test_connections(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return{
            "message":"Ket noi thanh cong"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Khong the ket noi {str(e)}")

# api them user
@app.post("/users", tags=["Users"], status_code=status.HTTP_201_CREATED)
def add_users(user:UserRequestDTo, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Them du lieu khong thanh cong")
    return {
        "status_code": 201,
        "message": "Them thanh cong",
        "data": db_user
    }

# api lay users
@app.get("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
def get_users(user_id:int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Khong tim thay du lieu")
    return {
        "status_code": 200,
        "message": "Lay du lieu thanh cong",
        "data": db_user
    }

# api cap nhat users
@app.put("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK )
def update_users(user_id:int, user:UserRequestDTo, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Khong tim thay du lieu")
    return {
        "status_code": 200,
        "message": "Cap nhat du lieu thanh cong",
        "data": db_user
    }

# api xoa users
@app.delete("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
def delete_users(user_id:int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Khong tim thay du lieu")
    db.delete(db_user)
    db.commit()
    return {
        "status_code": 200,
        "message": "Xoa du lieu thanh cong",
        "data": db_user
    }



# api tim kiem users
@app.get("/users/search", tags=["Users"], status_code=status.HTTP_200_OK)
def search_users(name: str = None, email: str = None, db: Session = Depends(get_db)):
    db_users = search_users(db, name=name, email=email)
    return {
        "status_code": 200,
        "message": "Tim kiem du lieu thanh cong",
        "data": db_users
    }


