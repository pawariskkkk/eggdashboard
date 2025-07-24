import pymysql
from sqlalchemy import create_engine, text

# --- Step 1: Connect to MySQL server (without specifying a database) ---
host = "localhost"
user = "root"
password = "1234"
port = 3306

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    port=port,
    autocommit=True  # so CREATE DATABASE applies immediately
)

cursor = connection.cursor()

# --- Step 2: Create database if not exists ---
cursor.execute("CREATE DATABASE IF NOT EXISTS egg_dashboard DEFAULT CHARACTER SET utf8;")

# --- Step 3: Connect to `egg_dashboard` database using SQLAlchemy ---
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/egg_dashboard")

# --- Step 4: Create tables with raw SQL (for partitioning support) ---
ddl = """
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
) ENGINE = InnoDB
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

CREATE TABLE IF NOT EXISTS real_time (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tray_number INT,
    date DATE NOT NULL,
    farm VARCHAR(45),
    house VARCHAR(45),
    mfg DATE NOT NULL,
    good_egg INT NOT NULL,
    dirty_egg INT NOT NULL,
    cam_status BOOLEAN,
    cam_id INT NOT NULL,
    tray_amount INT NOT NULL
) ENGINE = InnoDB;
"""

# Run the SQL using the SQLAlchemy engine
with engine.connect() as conn:
    for statement in ddl.strip().split(";"):
        if statement.strip():
            conn.execute(text(statement + ";"))

print("Database and tables created successfully.")
