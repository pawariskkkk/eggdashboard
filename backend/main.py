from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from datetime import datetime, date as date_type
from typing import Optional
from sqlalchemy.sql import text

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Then create partitioned tables manually via raw SQL
with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS egg (
        id BIGINT AUTO_INCREMENT,
        tray_number INT,
        date DATE NOT NULL,
        farm VARCHAR(45),
        house VARCHAR(45),
        mfg DATE NOT NULL,
        good_egg INT NOT NULL,
        dirty_egg INT NOT NULL,
        cam_status BOOLEAN,
        cam_id INT NOT NULL,
        tray_amount INT NOT NULL,
        PRIMARY KEY (id, date)
    )
    ENGINE=InnoDB
    PARTITION BY RANGE (YEAR(date)) (
        PARTITION p2025 VALUES LESS THAN (2026),
        PARTITION p2026 VALUES LESS THAN (2027),
        PARTITION p2027 VALUES LESS THAN (2028),
        PARTITION p2028 VALUES LESS THAN (2029),
        PARTITION p2029 VALUES LESS THAN (2030),
        PARTITION p2030 VALUES LESS THAN (2031),
        PARTITION p2031 VALUES LESS THAN (2032),
        PARTITION pmax VALUES LESS THAN MAXVALUE
    );
"""))

app = FastAPI(debug=True)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# Global flag (in-memory; not persistent)
api_status = {"enabled": True}

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
    
class ToggleData(BaseModel):
    enabled: bool

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
    
# Only allow these two tables
ALLOWED_TABLES = {
    "egg": "egg",
    "real_time": "real_time"
}

@app.get("/table_summary/{table_name}")
async def get_table_summary(table_name: str, db: Session = Depends(get_db)):
    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail="Invalid table name")

    selected_table = ALLOWED_TABLES[table_name]

    # Write slightly different query if needed, or same one for both
    query = text(f"""
        SELECT 
            date AS Date,
            farm AS Farm,
            house AS House,
            mfg AS "Manufacturing Date",
            (COALESCE(good_egg,0) + COALESCE(dirty_egg,0)) AS "Egg Amount",
            CASE 
                WHEN (COALESCE(good_egg,0) + COALESCE(dirty_egg,0)) > 0 THEN 
                    ROUND(COALESCE(dirty_egg,0) * 100.0 / (COALESCE(good_egg,0) + COALESCE(dirty_egg,0)), 2)
                ELSE 0
            END AS "Dirty Eggs %",
            tray_number AS "Tray Number"
        FROM {selected_table}
        WHERE tray_number > 0
    """)

    try:
        result = db.execute(query).fetchall()
        columns = result[0].keys() if result else []
        return [dict(zip(columns, row)) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

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
    
    if not api_status["enabled"]:
        raise HTTPException(status_code=403, detail="API is disabled.")

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
    
    new_tray1 = models.Egg(
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
    db.add(new_tray1)
    db.commit()
    db.refresh(new_tray)
    db.refresh(new_tray1)
    #to ping when post new data
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
    
@app.post("/toggle-api/")
def toggle_api(data: ToggleData):
    api_status["enabled"] = data.enabled
    return {"message": f"API status set to {data.enabled}"}
    
#add realtime table to egg table and delete realtime table after done
@app.delete("/finalize/", status_code=status.HTTP_200_OK)
async def finalize_realtime_session(db: Session = Depends(get_db)):
    # Step 1: Get all data from real_time table
    records = db.query(models.Real_time).all()

    if not records:
        return {"message": "No real-time data to finalize."}

    # Step 3: Delete all data from real_time table
    db.query(models.Real_time).delete()
    
    db.commit()

    return {"message": "Session ended. real_time cleared."}