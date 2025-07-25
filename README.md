# eggdashboard

for linux run this in the directory that container wait-for-it.sh: sudo chmod +x wait-for-it.sh

step1: docker compose up --build -d or only docker compose up -d if you already build


step2: set mysql workbench host:127.0.0.1 port:3307

to delete volumes and image: docker compose down --volumes --rmi all




To send images:
    send camera1 image to -> eggdashboard/frontend/images/camera1.jpg
    send camera2 image to -> eggdashboard/frontend/images/camera2.jpg

To post use postrealtime.py as template


command to create mysql database:
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema egg_dashboard
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema egg_dashboard
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `egg_dashboard` DEFAULT CHARACTER SET utf8 ;
USE `egg_dashboard` ;

-- -----------------------------------------------------
-- Table `egg_dashboard`.`table1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `egg_dashboard`.`egg` (
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

-- Create the `real_time` table (no partitioning)
CREATE TABLE IF NOT EXISTS `egg_dashboard`.`real_time` (
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

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


frontend
|-.streamlit: set auto rerun and theme
|-asset: collect image
|-images: get image from camera
|-app.py: main app
|-camera.py: camera components
|-chart.py: chart components
|-control.py: production control at the buttom of dashboard
|-dashboard.py: contain chart, control and camera realtime dashboard page
|-filter.py: contain filter that use for filter datatable
|-datatable.py: contain datatable
|-sidebar.py: sidebar of dashboard and datatable
|-style.css: style sidebar and container
|-utils.py: contain selectbox and function to style each container
|-fetch.py: fetch data from api
|-wait-for-it.sh: to make frontend start after backend

backend
|-database.py: to link with database mysql
|-main.py: fastapi
|-models.py: table models for database
