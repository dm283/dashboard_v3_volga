import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from app.database import Base


class GoodsUnderProcedure(Base):
    __tablename__ = 'goods_under_procedure'

    id = Column(Integer, primary_key=True)
    x1 = Column(String, default='0')
    x2 = Column(String, default='0')
    section = Column(String, default='0')
    created_datetime = Column(DateTime, default=datetime.datetime.now())


class GoodsProduced(Base):
    __tablename__ = 'goods_produced'

    id = Column(Integer, primary_key=True)
    x1 = Column(String, default='0')
    x2 = Column(String, default='0')
    section = Column(String, default='0')
    created_datetime = Column(DateTime, default=datetime.datetime.now())


class GoodsUsage(Base):
    __tablename__ = 'goods_usage'

    id = Column(Integer, primary_key=True)
    x1 = Column(String, default='0')
    x2 = Column(String, default='0')
    created_datetime = Column(DateTime, default=datetime.datetime.now())


class User(Base):
    __tablename__ = "users"
    login = Column(String, unique=True, index=True)
    type = Column(String)
    hashed_password = Column(String)
    id = Column(Integer, primary_key=True)
    comment = Column(String)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime, nullable=True, default=None)
    is_active = Column(Boolean, default=True)
