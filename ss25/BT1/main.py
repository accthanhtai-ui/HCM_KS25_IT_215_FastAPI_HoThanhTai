from pathlib import Path
import uuid

from fastapi import FastAPI, File, Form, UploadFile, HTTPException

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_COURSES = [
    "Python Basic",
    "FastAPI",
    "Data Analysis",
]

MAX_FILE_SIZE = 2 * 1024 * 1024


@app.post("/students/register")
async def register_student(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    course: str = Form(...),
    avatar: UploadFile = File(...),
):
    # Kiểm tra họ tên
    full_name = full_name.strip()

    if full_name == "":
        raise HTTPException(
            status_code=400,
            detail="Full name is required"
        )

    # Kiểm tra email
    email = email.strip()

    if "@" not in email:
        raise HTTPException(
            status_code=400,
            detail="Invalid email"
        )

    # Kiểm tra số điện thoại
    phone = phone.strip()

    if not phone.isdigit() or len(phone) != 10:
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number"
        )

    # Kiểm tra khóa học
    course = course.strip()

    if course not in ALLOWED_COURSES:
        raise HTTPException(
            status_code=400,
            detail="Course is not available"
        )

    # Kiểm tra định dạng ảnh
    extension = Path(avatar.filename).suffix.lower()

    if extension not in [".jpg", ".png"]:
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG files are allowed"
        )

    # Đọc file
    content = await avatar.read()

    # Kiểm tra kích thước file
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 2 MB"
        )

    # Tạo tên file mới, không dùng tên file người dùng gửi
    new_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / new_filename

    # Chỉ lưu file sau khi tất cả dữ liệu hợp lệ
    with open(file_path, "wb") as file:
        file.write(content)

    return {
        "success": True,
        "message": "Registration successful",
        "data": {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "course": course,
            "avatar": str(file_path),
        },
    }