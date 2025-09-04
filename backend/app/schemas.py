from datetime import datetime
from pydantic import BaseModel


class GoodsUnderProcedureCreate(BaseModel):
    x1: str | None = None
    x2: str | None = None
    x3: str | None = None
    x4: str | None = None
    x5: str | None = None
    x6: str | None = None
    x7: str | None = None
    x8: str | None = None
    x9: str | None = None
    x10: str | None = None
    x11: str | None = None
    x12: str | None = None
    x13: str | None = None
    x14: str | None = None
    x15: str | None = None
    x16: str | None = None
    x17: str | None = None
    x18: str | None = None
    x19: str | None = None
    x20: str | None = None
    x21: str | None = None
    x22: str | None = None
    x23: str | None = None
    x24: str | None = None
    x25: str | None = None
    x26: str | None = None
    x27: str | None = None
    x28: str | None = None
    x29: str | None = None
    x30: str | None = None
    x31: str | None = None
    x32: str | None = None
    x33: str | None = None
    x34: str | None = None
    x35: str | None = None
    x36: str | None = None
    section: str | None = None

class GoodsUnderProcedure(GoodsUnderProcedureCreate):
    id: int
    created_datetime: datetime
    class Config:
        from_attributes = True

###
class GoodsProducedCreate(BaseModel):
    x1: str | None = None
    x2: str | None = None
    x3: str | None = None
    x4: str | None = None
    x5: str | None = None
    x6: str | None = None
    x7: str | None = None
    section: str | None = None

class GoodsProduced(GoodsProducedCreate):
    id: int
    created_datetime: datetime
    class Config:
        from_attributes = True

###
class GoodsUsageCreate(BaseModel):
    x1: str | None = None
    x2: str | None = None
    x3: str | None = None
    x4: str | None = None
    x5: str | None = None
    x6: str | None = None
    x7: str | None = None
    x8: str | None = None
    x9: str | None = None
    x10: str | None = None
    x11: str | None = None
    x12: str | None = None
    x13: str | None = None
    x14: str | None = None

class GoodsUsage(GoodsUsageCreate):
    id: int
    created_datetime: datetime
    class Config:
        from_attributes = True

###
class UserBase(BaseModel):
    login: str
    type: str
    comment: str | None = None

class UserCreate(UserBase):
    password: str | None = None

class UserUpdate(UserBase):
    updated_datetime: datetime

class User(UserBase):
    id: int
    is_active: bool
    created_datetime: datetime
    updated_datetime: datetime | None
    class Config:
        from_attributes = True
