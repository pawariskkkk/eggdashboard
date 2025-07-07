from sqlalchemy import (
    Boolean, Column, Integer, String, Date, DateTime, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from database import Base


class Session(Base):
    __tablename__ = 'session'
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, primary_key=True, nullable=False)
    farm = Column(String(45), primary_key=True, nullable=False)
    house = Column(String(45), primary_key=True, nullable=False)
    mfg = Column(Date, primary_key=True, nullable=False)
    tray_amount = Column(Integer, nullable=False)

    trays = relationship("Tray", back_populates="session")


class Tray(Base):
    __tablename__ = 'tray'
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
            ['session_session_id', 'session_date', 'session_farm', 'session_house', 'session_mfg'],
            ['session.session_id', 'session.date', 'session.farm', 'session.house', 'session.mfg']
        ),
    )

    session = relationship("Session", back_populates="trays")