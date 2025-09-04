import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from app.database import Base


class GoodsUnderProcedure(Base):
    __tablename__ = 'goods_under_procedure'

    id = Column(Integer, primary_key=True)
    x1 = Column(String, default='0')
    x2 = Column(String, default='0')
    x3 = Column(String, default='0')
    x4 = Column(String, default='0')
    x5 = Column(String, default='0')
    x6 = Column(String, default='0')
    x7 = Column(String, default='0')
    x8 = Column(String, default='0')
    x9 = Column(String, default='0')
    x10 = Column(String, default='0')
    x11 = Column(String, default='0')
    x12 = Column(String, default='0')
    x13 = Column(String, default='0')
    x14 = Column(String, default='0')
    x15 = Column(String, default='0')
    x16 = Column(String, default='0')
    x17 = Column(String, default='0')
    x18 = Column(String, default='0')
    x19 = Column(String, default='0')
    x20 = Column(String, default='0')
    x21 = Column(String, default='0')
    x22 = Column(String, default='0')
    x23 = Column(String, default='0')
    x24 = Column(String, default='0')
    x25 = Column(String, default='0')
    x26 = Column(String, default='0')
    x27 = Column(String, default='0')
    x28 = Column(String, default='0')
    x29 = Column(String, default='0')
    x30 = Column(String, default='0')
    x31 = Column(String, default='0')
    x32 = Column(String, default='0')
    x33 = Column(String, default='0')
    x34 = Column(String, default='0')
    x35 = Column(String, default='0')
    x36 = Column(String, default='0')
    section = Column(String, default='0')
    created_datetime = Column(DateTime, default=datetime.datetime.now())


class GoodsProduced(Base):
    __tablename__ = 'goods_produced'

    id = Column(Integer, primary_key=True)
    x1 = Column(String, default='0')
    x2 = Column(String, default='0')
    x3 = Column(String, default='0')
    x4 = Column(String, default='0')
    x5 = Column(String, default='0')
    x6 = Column(String, default='0')
    x7 = Column(String, default='0')
    section = Column(String, default='0')
    created_datetime = Column(DateTime, default=datetime.datetime.now())


class GoodsUsage(Base):
    __tablename__ = 'goods_usage'

    id = Column(Integer, primary_key=True)
    x1 = Column(String, default='0')
    x2 = Column(String, default='0')
    x3 = Column(String, default='0')
    x4 = Column(String, default='0')
    x5 = Column(String, default='0')
    x6 = Column(String, default='0')
    x7 = Column(String, default='0')
    x8 = Column(String, default='0')
    x9 = Column(String, default='0')
    x10 = Column(String, default='0')
    x11 = Column(String, default='0')
    x12 = Column(String, default='0')
    x13 = Column(String, default='0')
    x14 = Column(String, default='0')
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
