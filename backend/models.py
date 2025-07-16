from sqlalchemy import (
    Boolean, Column, Integer, String, Date, BigInteger
)
from database import Base


class Egg(Base):
    __tablename__ = 'egg'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tray_number = Column(Integer)
    date = Column(Date, nullable=False, primary_key=True)
    farm = Column(String(45), nullable=True)
    house = Column(String(45), nullable=True)
    mfg = Column(Date, nullable=False)
    good_egg = Column(Integer, nullable=False)
    dirty_egg = Column(Integer, nullable=False)
    cam_status = Column(Boolean, nullable=True)
    cam_id = Column(Integer, nullable=False)
    tray_amount = Column(Integer, nullable=False)

class Real_time(Base):
    __tablename__ = 'real_time'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tray_number = Column(Integer)
    date = Column(Date, nullable=False)
    farm = Column(String(45), nullable=True)
    house = Column(String(45), nullable=True)
    mfg = Column(Date, nullable=False)
    good_egg = Column(Integer, nullable=False)
    dirty_egg = Column(Integer, nullable=False)
    cam_status = Column(Boolean, nullable=True)
    cam_id = Column(Integer, nullable=False)
    tray_amount = Column(Integer, nullable=False)