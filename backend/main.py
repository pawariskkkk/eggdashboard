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
    trays = db.query(models.Tray).filter(models.Tray.session_session_id == session_id).all()
    good_egg = sum([t.good_egg or 0 for t in trays])
    dirty_egg = sum([t.dirty_egg or 0 for t in trays])
    tray_count = len(trays)
    latest_tray = db.query(models.Tray).filter(models.Tray.session_session_id == session_id).order_by(models.Tray.tray_id.desc()).first()
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