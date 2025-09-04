from datetime import datetime
from pydantic import BaseModel


class GoodsUnderProcedureCreate(BaseModel):
    x1: str | None = None
    x2: str | None = None
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
