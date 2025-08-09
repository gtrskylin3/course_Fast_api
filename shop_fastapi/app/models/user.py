from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = 'users'
    
    id  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_supplier = Column(Boolean, default=False)
    is_customer = Column(Boolean, default=True)