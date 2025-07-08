from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Annotated
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

class SessionCreate(BaseModel):
    date: datetime
    farm: str
    house: str
    mfg: date_type
    tray_amount: int

class SessionSummary(BaseModel):
    good_egg: int
    dirty_egg: int
    tray_count: int
    cam1_status: Optional[bool]
    cam2_status: Optional[bool]
    cam1_image: Optional[str]
    cam2_image: Optional[str]

class RealTimeCreate(BaseModel):
    session_session_id: int
    tray_id: int  # Number to increment tray_id by (usually 1)
    good_egg: int
    dirty_egg: int
    cam1_status: Optional[bool] = None
    cam2_status: Optional[bool] = None
    cam1_image: Optional[str] = None
    cam2_image: Optional[str] = None

# ----------------------
# API Routes
# ----------------------

# Create a new session
@app.post("/session/", status_code=status.HTTP_201_CREATED)
async def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    db_session = models.Session(
        date=session.date,
        farm=session.farm,
        house=session.house,
        mfg=session.mfg,
        tray_amount=session.tray_amount
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return {
        "session_id": db_session.session_id,
        "date": db_session.date,
        "farm": db_session.farm,
        "house": db_session.house,
        "mfg": db_session.mfg,
        "tray_amount": db_session.tray_amount
    }

# Get session summary (good/dirty eggs, tray count, cam1/2 status/image from latest tray)
@app.get("/session/{session_id}/summary", response_model=SessionSummary, status_code=status.HTTP_200_OK)
async def get_session_summary(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    trays = db.query(models.Real_time).filter(models.Real_time.session_session_id == session_id).all()
    good_egg = sum([t.good_egg or 0 for t in trays])
    dirty_egg = sum([t.dirty_egg or 0 for t in trays])
    # tray_count is the highest tray_id for this session
    latest_tray = db.query(models.Real_time).filter(models.Real_time.session_session_id == session_id).order_by(models.Real_time.tray_id.desc()).first()
    tray_count = latest_tray.tray_id if latest_tray else 0
    cam1_status = latest_tray.cam1_status if latest_tray else None
    cam2_status = latest_tray.cam2_status if latest_tray else None
    cam1_image = latest_tray.cam1_image if latest_tray else None
    cam2_image = latest_tray.cam2_image if latest_tray else None
    return SessionSummary(
        good_egg=good_egg,
        dirty_egg=dirty_egg,
        tray_count=tray_count,
        cam1_status=cam1_status,
        cam2_status=cam2_status,
        cam1_image=cam1_image,
        cam2_image=cam2_image
    )

# ----------------------
# API Route to Post Real_time (Tray) Data
# ----------------------

@app.post("/real_time/", status_code=status.HTTP_201_CREATED)
async def create_real_time(data: RealTimeCreate, db: Session = Depends(get_db)):
    # Find the session in the Session model
    session_obj = db.query(models.Session).filter(models.Session.session_id == data.session_session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found for this session_id")

    # Get the latest tray for this session
    latest_tray = db.query(models.Real_time).filter(
        models.Real_time.session_session_id == data.session_session_id
    ).order_by(models.Real_time.tray_id.desc()).first()

    new_tray = models.Real_time(
        session_session_id=data.session_session_id,
        tray_id=(latest_tray.tray_id if latest_tray else 0) + data.tray_id,
        good_egg=data.good_egg,
        dirty_egg=data.dirty_egg,
        session_date=session_obj.date,
        session_farm=session_obj.farm,
        session_house=session_obj.house,
        session_mfg=session_obj.mfg,
        cam1_status=data.cam1_status,
        cam2_status=data.cam2_status,
        cam1_image=data.cam1_image,
        cam2_image=data.cam2_image
    )
    db.add(new_tray)
    db.commit()
    db.refresh(new_tray)
    return {
        "tray_id": new_tray.tray_id,
        "session_session_id": new_tray.session_session_id,
        "good_egg": new_tray.good_egg,
        "dirty_egg": new_tray.dirty_egg,
        "session_date": new_tray.session_date,
        "session_farm": new_tray.session_farm,
        "session_house": new_tray.session_house,
        "session_mfg": new_tray.session_mfg,
        "cam1_status": new_tray.cam1_status,
        "cam2_status": new_tray.cam2_status,
        "cam1_image": new_tray.cam1_image,
        "cam2_image": new_tray.cam2_image
    }