from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    profile = relationship(
        "UserProfileModel",
        back_populates="user",
        uselist=False
    )


class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    user = relationship(
        "UserModel",
        back_populates="profile"
    )


class ClassModel(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    class_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    class_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    max_students: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False
    )

    students = relationship(
        "StudentModel",
        back_populates="classroom"
    )


class StudentModel(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey("classes.id"),
        nullable=False
    )

    classroom = relationship(
        "ClassModel",
        back_populates="students"
    )

    enrollments = relationship(
        "EnrollmentModel",
        back_populates="student"
    )


class CourseModel(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    course_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    course_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    enrollments = relationship(
        "EnrollmentModel",
        back_populates="course"
    )


class EnrollmentModel(Base):
    __tablename__ = "enrollments"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "course_id",
            name="uq_student_course"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable=False
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )

    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="studying"
    )

    final_score: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    student = relationship(
        "StudentModel",
        back_populates="enrollments"
    )

    course = relationship(
        "CourseModel",
        back_populates="enrollments"
    )