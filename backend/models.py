from sqlalchemy import (
    Boolean, Column, Integer, String, Date, DateTime, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from database import Base


class Session(Base):
    __tablename__ = 'session'
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    farm = Column(String(45), nullable=False)
    house = Column(String(45), nullable=False)
    mfg = Column(Date, nullable=False)
    tray_amount = Column(Integer, nullable=False)

    realtime = relationship("Real_time", back_populates="session")


class Real_time(Base):
    __tablename__ = 'real_time'
    tray_id = Column(Integer, primary_key=True)
    session_session_id = Column(Integer, primary_key=True)
    session_date = Column(DateTime, nullable=False)
    session_farm = Column(String(45), nullable=False)
    session_house = Column(String(45), nullable=False)
    session_mfg = Column(Date, nullable=False)
    good_egg = Column(Integer, nullable=False)
    dirty_egg = Column(Integer, nullable=False)
    cam1_status = Column(Boolean, nullable=True)
    cam2_status = Column(Boolean, nullable=True)
    cam1_image = Column(String(100), nullable=True)
    cam2_image = Column(String(100), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['session_session_id'],
            ['session.session_id']
        ),
    )

    session = relationship("Session", back_populates="realtime")