from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
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

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    address = Column(
        String(255),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    user = relationship(
        "UserModel",
        back_populates="profile"
    )


class ClassroomModel(Base):
    __tablename__ = "classrooms"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    class_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    class_name = Column(
        String(100),
        nullable=False
    )

    max_students = Column(
        Integer,
        nullable=False
    )

    status = Column(
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

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    gender = Column(
        String(10),
        nullable=False
    )

    class_id = Column(
        Integer,
        ForeignKey("classrooms.id"),
        nullable=False
    )

    classroom = relationship(
        "ClassroomModel",
        back_populates="students"
    )

    enrollments = relationship(
        "EnrollmentModel",
        back_populates="student"
    )


class CourseModel(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    course_name = Column(
        String(100),
        nullable=False
    )

    enrollments = relationship(
        "EnrollmentModel",
        back_populates="course"
    )


class EnrollmentModel(Base):
    __tablename__ = "enrollments"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    status = Column(
        String(20),
        default="studying"
    )

    final_score = Column(
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