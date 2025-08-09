from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from app.backend.db import Base
from app.models import *


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey('categories.id'),
                       nullable=True, default=None)

    products = relationship('Product', back_populates='category')

    # def __repr__(self):
    #     return f"Category(id={self.id}, name='{self.name}', slug='{self.slug}')"
