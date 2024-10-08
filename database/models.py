from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


# Создание таблиці груп
class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


# Создание таблицы студентів
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(100), nullable=True)
    group_id = Column("group_id", ForeignKey("groups.id", ondelete="CASCADE"))
    group = relationship("Group", backref="students")

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


# Создание таблиці викладачів
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column("email", String(100), nullable=False)
    address = Column("address", String(100), nullable=True)
    start_work = Column(Date, nullable=True)

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


# Создание таблиці предметів із вказівкою викладача
class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column("teacher_id", ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher = relationship("Teacher", backref="subjects")


# Создание таблиці оцінок студентів з предметів
class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column("date_of", Date, nullable=True)
    student_id = Column("student_id", ForeignKey("students.id", ondelete="CASCADE"))
    subject_id = Column("subject_id", ForeignKey("subjects.id", ondelete="CASCADE"))
    student = relationship("Student", backref="grade")
    subject = relationship("Subject", backref="grade")
