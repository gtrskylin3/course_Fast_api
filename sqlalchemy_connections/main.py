from typing import List
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey


class Base(DeclarativeBase):
    pass


"""В отношениях один к одному первичный 
ключ одной таблицы служит ключом в другой таблице, 
устанавливая прямую связь между двумя сущностями.
Этот тип отношений обычно используется, 
когда существует строгое соответствие один к одному 
между моделируемыми сущностями. Например, рассмотрим сценарий, 
в котором у вас есть таблица "Пользователей" и таблица "Профилей". 
У каждого пользователя есть один профиль, 
и каждый профиль принадлежит только одному пользователю."""


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String())
    profile = relationship("Profile", uselist=False, back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")


# указав имя другой модели и параметр uselist=False
# для обозначения отношения один к одному.
# Параметр back_populates обеспечивает двунаправленную навигацию,
# обеспечивая доступ к связанному объекту User из объекта Profile
#  и от объекта User к объекту Profile

"""
Oтношения один ко многим в SQLAlchemy представляют
собой общую связь между двумя сущностями, 
где одна запись в одной таблице связана с несколькими 
записями в другой таблице. В отношениях "один ко-многим" 
первичный ключ экземпляра "одной" стороны служит в качестве
внешнего ключа в экземпляре "много" стороны, 
устанавливая иерархическую связь. 
Этот тип отношений часто используется, 
когда один экземпляр имеет несколько связанных с ним экземпляров. 
Например, рассмотрим сценарий, в котором 
у вас есть модель "Отдел" и модель "Сотрудник".
"""

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    employees = relationship("Employee", back_populates='department')


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates='employees')

# В отличие от отношений "один к одному", 
# мы не используем параметр uselist=False, так как хотим, 
# чтобы многие сотрудники могли быть связаны с одним отделом. 
# employees: Mapped[List["Employee"]] = relationship("Employee", backref="department")

"""
Многие ко многим отношения представляют собой сложную 
связь между двумя моделями, где несколько записей 
в одной таблице могут быть связаны с несколькими записями 
в другой таблице. В отношениях "многие ко многим" 
для установления связи между двумя моделями используется
 посредническая таблица. Например, рассмотрим сценарий, 
в котором у вас есть модель "Студент" и модель "Курс".
"""

# SQLAlchemy предоставляет простой способ реализации отношений 
# "многие ко многим". Для этого вам нужно ввести посредническую 
# таблицу, также известную как таблица соединений 
# или таблица ассоциаций, которая фиксирует связи 
# между двумя другими моделями. Эта посредническая 
# таблица содержит внешние ключи обоих объектов, 
# что позволяет установить отношения "многие ко многим".

class StudentCourses(Base):
    __tablename__ = 'student_courses'
    id =  id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    courses = relationship('Course',
            secondary=StudentCourses.__table__,
            back_populates='students')

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    students = relationship('Student',
            secondary=StudentCourses.__table__,
            back_populates='courses')

