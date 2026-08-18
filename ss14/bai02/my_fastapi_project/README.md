# Student Management API (FastAPI + MySQL)

Run the app:

1. Set `DATABASE_URL` environment variable (example):

```
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/students_db"
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Start server:

```
uvicorn my_fastapi_project.main:app --reload
```

Files of note:

- [my_fastapi_project/main.py](my_fastapi_project/main.py)
- [my_fastapi_project/app/database.py](my_fastapi_project/app/database.py)
- [my_fastapi_project/app/models/student.py](my_fastapi_project/app/models/student.py)
- [my_fastapi_project/app/schemas/student.py](my_fastapi_project/app/schemas/student.py)
- [my_fastapi_project/app/services/student.py](my_fastapi_project/app/services/student.py)
- [my_fastapi_project/app/routers/student.py](my_fastapi_project/app/routers/student.py)
