# BÁO CÁO LỖI CẤU HÌNH QUAN HỆ - HỆ THỐNG QUẢN LÝ DỰ ÁN

## Lỗi 1: Quan hệ 1 - 1 (Employee ↔ Device)

**Tên lỗi:** Thiếu ràng buộc UNIQUE trên khóa ngoại, khiến quan hệ 1-1 bị biến thành 1-N.

**Vị trí dòng code gây lỗi:**
```python
employee_id = Column(Integer, ForeignKey("employees.id"))
```
(trong class `Device`)

**Nguyên nhân gây lỗi:**
ForeignKey chỉ đảm bảo tính toàn vẹn tham chiếu (giá trị `employee_id` phải tồn tại trong bảng `employees`), chứ không giới hạn số lần một `employee_id` được lặp lại trong bảng `devices`. Vì cột này không có `unique=True`, nhiều dòng `Device` khác nhau có thể cùng trỏ về một `employee_id`, dẫn đến một nhân viên có thể được cấp phát nhiều thiết bị, phá vỡ quy tắc 1-1.

**Cách khắc phục:**
Sửa từ:
```python
employee_id = Column(Integer, ForeignKey("employees.id"))
```
thành:
```python
employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
```

---

## Lỗi 2: Quan hệ 1 - N (Department ↔ Employee)

**Tên lỗi:** Lỗi đồng bộ hai chiều `back_populates` trỏ sai tên thuộc tính.

**Vị trí dòng code gây lỗi:**
```python
employees = relationship("Employee", back_populates="department_id")
```
(trong class `Department`)

**Nguyên nhân gây lỗi:**
`back_populates` phải trỏ tới tên thuộc tính `relationship` ở phía đối diện, không phải tên cột (Column). Ở đây `department_id` là một `Column` khóa ngoại trong `Employee`, còn thuộc tính `relationship` thật sự trong `Employee` có tên là `department`. Do đặt sai tên, SQLAlchemy không thể ánh xạ hai chiều quan hệ, khiến việc truy cập danh sách nhân viên từ Phòng ban (và ngược lại) bị lỗi.

**Cách khắc phục:**
Sửa từ:
```python
employees = relationship("Employee", back_populates="department_id")
```
thành:
```python
employees = relationship("Employee", back_populates="department")
```

---

## Lỗi 3: Quan hệ N - N (Employee ↔ Project)

**Tên lỗi:** Thiếu khai báo bảng trung gian (`secondary`) trong cấu hình relationship.

**Vị trí dòng code gây lỗi:**
```python
projects = relationship("Project", back_populates="employees")
```
(trong class `Employee`)
```python
employees = relationship("Employee", back_populates="projects")
```
(trong class `Project`)

**Nguyên nhân gây lỗi:**
Quan hệ N-N trong SQLAlchemy bắt buộc phải khai báo tham số `secondary` để chỉ định bảng trung gian dùng lưu các cặp liên kết. Dù bảng `employee_project` đã được tạo sẵn, nhưng không có `relationship` nào tham chiếu đến nó, nên SQLAlchemy không biết dùng bảng nào để lưu/truy vấn việc phân công nhân viên vào dự án, gây ra lỗi thiếu cấu hình liên kết bảng trung gian.

**Cách khắc phục:**
Sửa từ:
```python
projects = relationship("Project", back_populates="employees")
```
thành:
```python
projects = relationship("Project", secondary=employee_project, back_populates="employees")
```

Và sửa từ:
```python
employees = relationship("Employee", back_populates="projects")
```
thành:
```python
employees = relationship("Employee", secondary=employee_project, back_populates="projects")
```

---

## Tổng kết

| STT | Quan hệ | Lỗi | Cách sửa |
|-----|---------|-----|----------|
| 1 | 1 - 1 (Employee ↔ Device) | Thiếu `unique=True` trên khóa ngoại `employee_id` | Thêm `unique=True` |
| 2 | 1 - N (Department ↔ Employee) | `back_populates` trỏ sai tên (dùng tên Column thay vì tên relationship) | Đổi `back_populates="department_id"` thành `back_populates="department"` |
| 3 | N - N (Employee ↔ Project) | Thiếu tham số `secondary` trỏ tới bảng trung gian | Thêm `secondary=employee_project` vào cả hai relationship |
