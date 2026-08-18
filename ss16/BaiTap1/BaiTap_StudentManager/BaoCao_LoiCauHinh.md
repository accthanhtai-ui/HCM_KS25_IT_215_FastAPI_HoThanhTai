# BÁO CÁO LỖI CẤU HÌNH QUAN HỆ - HỆ THỐNG QUẢN LÝ SINH VIÊN

## Lỗi 1: Quan hệ 1 - 1 (Student ↔ Profile)

**Tên lỗi:** Thiếu ràng buộc UNIQUE trên khóa ngoại, khiến quan hệ 1-1 bị biến thành 1-N.

**Vị trí dòng code gây lỗi:**
```python
student_id = Column(Integer, ForeignKey("students.id"))
```
(trong class `Profile`)

**Nguyên nhân gây lỗi:**
Trong SQLAlchemy, khóa ngoại (ForeignKey) chỉ đảm bảo tính toàn vẹn tham chiếu, chứ không tự động giới hạn số lượng bản ghi liên kết. Nếu cột `student_id` không được đánh dấu là duy nhất (`unique=True`), thì nhiều dòng khác nhau trong bảng `profiles` đều có thể trỏ tới cùng một `student_id`. Điều này khiến một sinh viên có thể có nhiều hồ sơ (Profile), tức là quan hệ thực chất trở thành 1-N chứ không còn là 1-1 nữa.

**Cách khắc phục:**
Sửa từ:
```python
student_id = Column(Integer, ForeignKey("students.id"))
```
thành:
```python
student_id = Column(Integer, ForeignKey("students.id"), unique=True)
```

---

## Lỗi 2: Quan hệ 1 - N (Department ↔ Student)

**Tên lỗi:** Lỗi đồng bộ hai chiều `back_populates` trỏ sai tên thuộc tính.

**Vị trí dòng code gây lỗi:**
```python
students = relationship("Student", back_populates="department_id")
```
(trong class `Department`)

**Nguyên nhân gây lỗi:**
`back_populates` phải trỏ đến tên của thuộc tính `relationship` ở phía bên kia, chứ không phải tên của cột (Column) khóa ngoại. Ở đây, `department_id` là một `Column` (khóa ngoại), không phải một `relationship`. Trong khi đó, thuộc tính `relationship` thật sự ở phía `Student` có tên là `department`. Vì cấu hình sai tên, SQLAlchemy không thể liên kết hai thuộc tính với nhau, dẫn đến việc không thể truy cập danh sách sinh viên từ đối tượng Khoa và ngược lại.

**Cách khắc phục:**
Sửa từ:
```python
students = relationship("Student", back_populates="department_id")
```
thành:
```python
students = relationship("Student", back_populates="department")
```

---

## Lỗi 3: Quan hệ N - N (Student ↔ Course)

**Tên lỗi:** Thiếu khai báo bảng trung gian (`secondary`) trong cấu hình relationship.

**Vị trí dòng code gây lỗi:**
```python
courses = relationship("Course", back_populates="students")
```
(trong class `Student`)
```python
students = relationship("Student", back_populates="courses")
```
(trong class `Course`)

**Nguyên nhân gây lỗi:**
Quan hệ N-N trong SQLAlchemy bắt buộc phải thông qua một bảng trung gian (association table), và bảng đó phải được khai báo tường minh bằng tham số `secondary` trong `relationship()`. Mặc dù bảng `student_course` đã được tạo ở đầu file, nhưng không có `relationship` nào tham chiếu tới nó. Do đó SQLAlchemy không biết phải dùng bảng nào để lưu và truy vấn các cặp liên kết giữa Student và Course, dẫn đến lỗi không tìm thấy cấu hình bảng liên kết trung gian khi sinh viên đăng ký môn học.

**Cách khắc phục:**
Sửa từ:
```python
courses = relationship("Course", back_populates="students")
```
thành:
```python
courses = relationship("Course", secondary=student_course, back_populates="students")
```

Và sửa từ:
```python
students = relationship("Student", back_populates="courses")
```
thành:
```python
students = relationship("Student", secondary=student_course, back_populates="courses")
```

---

## Tổng kết

| STT | Quan hệ | Lỗi | Cách sửa |
|-----|---------|-----|----------|
| 1 | 1 - 1 (Student ↔ Profile) | Thiếu `unique=True` trên khóa ngoại | Thêm `unique=True` vào `student_id` |
| 2 | 1 - N (Department ↔ Student) | `back_populates` trỏ sai tên (dùng tên Column thay vì tên relationship) | Đổi `back_populates="department_id"` thành `back_populates="department"` |
| 3 | N - N (Student ↔ Course) | Thiếu tham số `secondary` trỏ tới bảng trung gian | Thêm `secondary=student_course` vào cả hai relationship |
