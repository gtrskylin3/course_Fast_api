from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from typing import Optional
from app.backend.db import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

from sqlalchemy.schema import CreateTable
print(CreateTable(Category.__table__))