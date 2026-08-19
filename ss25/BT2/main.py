from pathlib import Path
import uuid

from fastapi import FastAPI, File, Form, UploadFile, HTTPException

app = FastAPI()

UPLOAD_FOLDER = Path("storage/documents")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ".ppt", ".pptx"]

ALLOWED_DOCUMENT_TYPES = [
    "lecture",
    "assignment",
    "reference",
]

MAX_FILE_SIZE = 10 * 1024 * 1024


@app.post("/documents")
async def upload_document(
    title: str = Form(...),
    course_code: str = Form(...),
    document_type: str = Form(...),
    description: str = Form(""),
    document: UploadFile = File(...),
):
    # Kiểm tra tên tài liệu
    title = title.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    # Chuẩn hóa mã môn học
    course_code = course_code.strip().upper()

    if course_code == "":
        raise HTTPException(
            status_code=400,
            detail="Course code is required"
        )

    # Kiểm tra loại tài liệu
    document_type = document_type.strip().lower()

    if document_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Document type is not allowed"
        )

    # Lấy phần mở rộng bằng Path.suffix
    extension = Path(document.filename).suffix.lower()

    # Kiểm tra phần mở rộng
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type is not allowed"
        )

    # Đọc file
    content = await document.read()

    # Kiểm tra file rỗng
    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="File cannot be empty"
        )

    # Kiểm tra kích thước file
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB"
        )

    # Lưu tên file gốc
    original_filename = document.filename

    # Tạo tên file mới để tránh trùng
    stored_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_FOLDER / stored_filename

    # Lưu file
    with open(file_path, "wb") as output_file:
        output_file.write(content)

    return {
        "success": True,
        "message": "Document uploaded successfully",
        "data": {
            "title": title,
            "course_code": course_code,
            "document_type": document_type,
            "description": description,
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "file_path": str(file_path),
        },
    }