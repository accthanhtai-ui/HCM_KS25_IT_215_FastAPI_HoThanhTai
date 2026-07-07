#file này chỉ dùng để cấu hình kết nối dtb
#dùng thu viện sqlalchemy giúp kết nối với my sql
#tải thư viện về - pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
#bước 1 cấu hình connection tới database
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/school_db"
#bước 2: bộ điều phối kết nối vật lí (connection pool)
engine = create_engine(DATABASE_URL)
#bươc 3: tạo ra localsession để gửi dữ liệu 
localSession = sessionmaker(
    autocommit =  False,
    autoflush=False,
    bind = engine
)
Base = declarative_base()
#bước 4 : tạo hàm để gọi dữ liệu để chạy
def get_db():
    try:
        db=localSession()
        yield db
        pass
    except:
        db.close()