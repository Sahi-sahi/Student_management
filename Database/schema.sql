-- ============================================================
--  Student Management System - Database Schema
--  Run this file once to set up the MySQL database
-- ============================================================

CREATE DATABASE IF NOT EXISTS myproject_db;
USE myproject_db;

CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE
);

INSERT IGNORE INTO departments (name, code) VALUES
('Computer Science', 'CS'),
('Electronics & Communication', 'ECE'),
('Mechanical Engineering', 'ME'),
('Civil Engineering', 'CE'),
('Information Technology', 'IT'),
('Business Administration', 'MBA');

CREATE TABLE IF NOT EXISTS students (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    student_id  VARCHAR(20) NOT NULL UNIQUE,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    phone       VARCHAR(15),
    dob         DATE,
    gender      ENUM('Male', 'Female', 'Other') NOT NULL DEFAULT 'Male',
    department_id INT,
    year        INT CHECK (year BETWEEN 1 AND 6),
    gpa         DECIMAL(3,2) CHECK (gpa BETWEEN 0.00 AND 10.00),
    address     TEXT,
    status      ENUM('Active', 'Inactive', 'Graduated', 'Suspended') DEFAULT 'Active',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS activity_log (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    action     VARCHAR(50) NOT NULL,
    student_id VARCHAR(20),
    details    TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
