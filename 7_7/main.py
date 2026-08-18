from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import text
from database import Base,engine
from model import StudentModel
Sesion = 0

app = FastAPI(
    title="demo connection database"
)
#dùng để khai báo yêu cầu python gửi yêu cầu tới dtb tạo bảng
Base.metadata.create_all(bind = engine)


@app.get("/test-connection")
def test_connection(db:Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "message": "kết nối thành công"
        }
    except Exception as e:
        raise HTTPException(status_code=404,detail=f"lỗi không kết nối được {str(e)}")