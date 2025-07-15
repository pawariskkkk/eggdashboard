from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from datetime import datetime, date as date_type
from typing import Optional

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



# ----------------------
# Pydantic Schemas
# ----------------------

class FirstCreate(BaseModel):
    date: datetime
    farm: str
    house: str
    mfg: date_type
    tray_amount: int

class SessionSummary(BaseModel):
    good_egg: int
    dirty_egg: int
    tray_count: int
    cam_status: Optional[bool]

class RealTimeCreate(BaseModel):
    tray_number: int  # Number to increment tray_number by (usually 1)
    good_egg: int
    dirty_egg: int
    cam_status: Optional[bool] = None
    cam_id: int
# ----------------------
# API Routes
# ----------------------

# Get session summary (good/dirty eggs, tray count, cam1/2 status/image from latest tray)
@app.get("/session/{cam_id}/summary", response_model=SessionSummary, status_code=status.HTTP_200_OK)
async def get_session_summary(cam_id: int, db: Session = Depends(get_db)):
    trays = db.query(models.Real_time).all()
    good_egg = sum([t.good_egg or 0 for t in trays])
    dirty_egg = sum([t.dirty_egg or 0 for t in trays])
    # tray_count is the highest tray_number for this session
    latest_tray = db.query(models.Real_time).order_by(models.Real_time.tray_number.desc()).first()
    latest_cam = db.query(models.Real_time).filter(models.Real_time.cam_id == cam_id).order_by(models.Real_time.tray_number.desc()).first()
    tray_count = latest_tray.tray_number if latest_tray else 0
    cam_status = latest_cam.cam_status if latest_cam else None
    return SessionSummary(
        good_egg=good_egg,
        dirty_egg=dirty_egg,
        tray_count=tray_count,
        cam_status=cam_status,
    )

# ----------------------
# API Route to Post Real_time (Tray) Data
# ----------------------
@app.post("/firsttime/", status_code=status.HTTP_201_CREATED)
async def create_firsttime(data: FirstCreate, db: Session = Depends(get_db)):
    db_session = models.Real_time(
        date=data.date,
        farm=data.farm,
        house=data.house,
        mfg=data.mfg,
        tray_amount=data.tray_amount,
        good_egg=0,
        dirty_egg=0,
        cam_id=1,
        tray_number=0
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return {
        "date": db_session.date,
        "farm": db_session.farm,
        "house": db_session.house,
        "mfg": db_session.mfg,
        "tray_amount": db_session.tray_amount
    }

@app.post("/real_time/", status_code=status.HTTP_201_CREATED)
async def create_real_time(data: RealTimeCreate, db: Session = Depends(get_db)):

    # Get the latest tray for this session
    latest_tray = db.query(models.Real_time).order_by(models.Real_time.tray_number.desc()).first()

    new_tray = models.Real_time(
        tray_number=(latest_tray.tray_number if latest_tray else 0) + data.tray_number,
        good_egg=data.good_egg,
        dirty_egg=data.dirty_egg,
        date=latest_tray.date,
        farm=latest_tray.farm,
        house=latest_tray.house,
        tray_amount=latest_tray.tray_amount,
        mfg=latest_tray.mfg,
        cam_status=data.cam_status,
        cam_id=data.cam_id,
    )
    db.add(new_tray)
    db.commit()
    db.refresh(new_tray)
    with open("/shared/ping.flag", "w") as f:
        f.write("1")
    
    return {
        "tray_number": new_tray.tray_number,
        "good_egg": new_tray.good_egg,
        "dirty_egg": new_tray.dirty_egg,
        "date": new_tray.date,
        "farm": new_tray.farm,
        "house": new_tray.house,
        "mfg": new_tray.mfg,
        "cam_status": new_tray.cam_status,
        "cam_id": new_tray.cam_id,
    }
    
@app.post("/finalize/", status_code=status.HTTP_201_CREATED)
def finalize_realtime_session(db: Session = Depends(get_db)):
    # Step 1: Get all data from real_time table
    records = db.query(models.Real_time).all()

    if not records:
        return {"message": "No real-time data to finalize."}

    # Step 2: Move each record to Egg table
    for record in records:
        egg = models.Egg(
            tray_number=record.tray_number,
            date=record.date,
            farm=record.farm,
            house=record.house,
            mfg=record.mfg,
            good_egg=record.good_egg,
            dirty_egg=record.dirty_egg,
            cam_status=record.cam_status,
            cam_id=record.cam_id,
            tray_amount=record.tray_amount
        )
        db.add(egg)

    # Step 3: Delete all data from real_time table
    db.query(models.Real_time).delete()
    
    db.commit()

    return {"message": "Session ended. Data moved to Egg table and real_time cleared."}