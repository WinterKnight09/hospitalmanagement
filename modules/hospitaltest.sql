
CREATE DATABASE IF NOT EXISTS hospitaltests;

USE hospitaltests;

CREATE TABLE IF NOT EXISTS app_users (
    user_id     INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    password    VARCHAR(255) NOT NULL,
    role        VARCHAR(100) NOT NULL,
    age         INT NOT NULL,
    gender      VARCHAR(20) NOT NULL,
    address     VARCHAR(255),
    mobile_no   VARCHAR(10) NOT NULL UNIQUE,
    experience  INT DEFAULT 0
);


INSERT INTO app_users
(name, password, role, age, gender, address, mobile_no, experience)
VALUES
('Dr. Priya Sharma',   'Doctor@123',  'Doctor',       38, 'Female', '45, T Nagar, Chennai',    '9840123456', 14),
('siddharth', 'Doctor@456',  'Doctor',       42, 'Male',   '7, Porur, Chennai',       '9884365552', 18),
('Meena Lakshmi',      'Recept@123',  'Receptionist', 27, 'Female', '23, Velachery, Chennai',  '9962345678', 3),
('Karthik Raja',       'Recept@456',  'Receptionist', 30, 'Male',   '88, Tambaram, Chennai',   '9791234567', 6);
insert into app_users (name, password, role, age, gender, address, mobile_no, experience) values ('Siddharth', 'Nopassword@090825',  'admin',       53, 'Male',   '11a, Porur, Chennai','9884365550', 22);
SELECT * FROM app_users;

CREATE TABLE PATIENT_REGISTRATION
(
    PATIENT_ID INT AUTO_INCREMENT PRIMARY KEY,
    PATIENT_NAME VARCHAR(100) NOT NULL,
    DOB DATE NOT NULL,
    AGE INT NOT NULL,
    GENDER VARCHAR(15) NOT NULL,
    ADDRESS VARCHAR(255) NOT NULL,
    ID_PROOF_TYPE VARCHAR(50) NOT NULL,
    ID_PROOF_NUMBER VARCHAR(100) NOT NULL,
    MOBILE_NUMBER VARCHAR(15) NOT NULL,
    SECONDARY_NUMBER VARCHAR(15),
    EMAIL VARCHAR(100),
    PROFESSION VARCHAR(100) NOT NULL,
    INCOME DECIMAL(12,2),
    EMERGENCY_CONTACT VARCHAR(15),
    BLOOD_GROUP VARCHAR(5),
    PATIENT_TYPE ENUM('Inpatient', 'Outpatient') NOT NULL,
    REGISTRATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select*from PATIENT_REGISTRATION;
