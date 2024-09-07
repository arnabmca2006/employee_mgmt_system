--DDL commands

CREATE SCHEMA IF NOT EXISTS ems AUTHORIZATION postgres;


CREATE TABLE IF NOT EXISTS ems.department
(
    department_id VARCHAR(25) NOT NULL,
    name VARCHAR(25) UNIQUE NOT NULL,
    location VARCHAR(50) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    created_by text NOT NULL,
    updated_on timestamp with time zone NULL,
    updated_by text NULL,
    CONSTRAINT department_pkey PRIMARY KEY (department_id)
);
ALTER TABLE ems.department OWNER TO postgres;


CREATE TABLE IF NOT EXISTS ems.employee
(
    employee_id VARCHAR(25) NOT NULL,
    department_id VARCHAR(25) NOT NULL,
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(25) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(6) NOT NULL,
    nationality VARCHAR(20) NOT NULL,
    hire_date DATE NOT NULL,
    job_title VARCHAR(20) NOT NULL,
    email VARCHAR(25) NULL,
    phone_number VARCHAR(20) NULL,
    address VARCHAR(50) NOT NULL,
    salary NUMERIC NULL default 0.00,
    created_on timestamp with time zone NOT NULL,
    created_by text NOT NULL,
    updated_on timestamp with time zone NULL,
    updated_by text NULL,
    CONSTRAINT employee_pkey PRIMARY KEY (employee_id),
    CONSTRAINT department_id_fk FOREIGN KEY (department_id) REFERENCES ems.department (department_id) ON DELETE CASCADE
);
ALTER TABLE ems.employee OWNER TO postgres;


CREATE TABLE IF NOT EXISTS ems.salary_breakup
(
    salary_id BIGSERIAL NOT NULL,
    employee_id VARCHAR(25) NOT NULL,
    effective_date DATE NOT NULL,
    basic_salary NUMERIC NOT NULL default 0.00,
    allowances NUMERIC NOT NULL default 0.00,
    deductions NUMERIC NOT NULL default 0.00,
    total_salary NUMERIC NOT NULL default 0.00,
    created_on timestamp with time zone NOT NULL,
    created_by text NOT NULL,
    updated_on timestamp with time zone NULL,
    updated_by text NULL,
    CONSTRAINT salary_id_pkey PRIMARY KEY (salary_id),
    CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES ems.employee (employee_id) ON DELETE CASCADE
);
ALTER TABLE ems.salary_breakup OWNER TO postgres;


--DML commands

--Insert Sample Data into department Table
INSERT INTO ems.department (
    department_id, name, location, created_on, created_by
) VALUES
('DEPT001', 'Engineering', 'Springfield', NOW(), 'admin'),
('DEPT002', 'Quality Assurance', 'Springfield', NOW(), 'admin'),
('DEPT003', 'IT Support', 'Springfield', NOW(), 'admin');


--Insert Sample Data into employee Table
INSERT INTO ems.employee (
    employee_id, first_name, last_name, date_of_birth, gender, nationality, hire_date, job_title, department_id, Email, phone_number, address, salary, created_on, created_by
) VALUES
('EMP001', 'Alice', 'Johnson', '1985-02-15', 'Female', 'American', '2010-05-01', 'Software Engineer', 'DEPT001', 'alice.johnson@example.com', '555-1234', '123 Elm St, Springfield', 48000.00, NOW(), 'admin'),
('EMP002', 'Bob', 'Smith', '1990-06-20', 'Male', 'American', '2012-08-15', 'Project Manager', 'DEPT001', 'bob.smith@example.com', '555-5678', '456 Oak St, Springfield', 54000.00, NOW(), 'admin'),
('EMP003', 'Carol', 'Davis', '1987-11-10', 'Female', 'American', '2015-01-25', 'QA Analyst', 'DEPT002', 'carol.davis@example.com', '555-8765', '789 Pine St, Springfield', 57500.00, NOW(), 'admin'),
('EMP004', 'David', 'Brown', '1989-03-30', 'Male', 'Canadian', '2018-09-10', 'DevOps Engineer', 'DEPT002', 'david.brown@example.com', '555-4321', '321 Maple St, Springfield', 50500.00, NOW(), 'admin'),
('EMP005', 'Emma', 'Wilson', '1992-07-22', 'Female', 'British', '2017-06-18', 'UI/UX Designer', 'DEPT001', 'emma.wilson@example.com', '555-3456', '654 Cedar St, Springfield', 51000.00, NOW(), 'admin'),
('EMP006', 'Frank', 'Taylor', '1986-12-01', 'Male', 'American', '2011-03-14', 'Network Engineer', 'DEPT003', 'frank.taylor@example.com', '555-6789', '987 Birch St, Springfield', 55900.00, NOW(), 'admin'),
('EMP007', 'Grace', 'Lee', '1994-04-18', 'Female', 'American', '2020-07-02', 'Business Analyst', 'DEPT001', 'grace.lee@example.com', '555-3456', '654 Maple St, Springfield', 55500.00, NOW(), 'admin'),
('EMP008', 'Henry', 'Moore', '1983-08-25', 'Male', 'American', '2009-11-20', 'Database Admin', 'DEPT002', 'henry.moore@example.com', '555-6789', '987 Birch St, Springfield', 57800.00, NOW(), 'admin'),
('EMP009', 'Ivy', 'Martin', '1991-05-14', 'Female', 'Canadian', '2019-02-13', 'Marketing Manager', 'DEPT003', 'ivy.martin@example.com', '555-1234', '123 Birch St, Springfield', 59800.00, NOW(), 'admin'),
('EMP010', 'Jack', 'Anderson', '1988-10-09', 'Male', 'American', '2013-04-30', 'System Analyst', 'DEPT002', 'jack.anderson@example.com', '555-5678', '456 Elm St, Springfield', 59500.00, NOW(), 'admin');

INSERT INTO ems.salary_breakup (
    employee_id, effective_date, basic_salary, allowances, deductions, total_salary, created_on, created_by
) VALUES
('EMP001', '2024-01-01', 50000.00, 5000.00, 2000.00, 48000.00, NOW(), 'admin'),
('EMP002', '2024-01-01', 55000.00, 4500.00, 1500.00, 54000.00, NOW(), 'admin'),
('EMP003', '2024-01-01', 60000.00, 6000.00, 2500.00, 57500.00, NOW(), 'admin'),
('EMP004', '2024-02-01', 52000.00, 5500.00, 1800.00, 50500.00, NOW(), 'admin'),
('EMP005', '2024-02-01', 53000.00, 6000.00, 2000.00, 51000.00, NOW(), 'admin'),
('EMP006', '2024-03-01', 58000.00, 6200.00, 2100.00, 55900.00, NOW(), 'admin'),
('EMP007', '2024-03-01', 59000.00, 6500.00, 2300.00, 55500.00, NOW(), 'admin'),
('EMP008', '2024-04-01', 60000.00, 7000.00, 2200.00, 57800.00, NOW(), 'admin'),
('EMP009', '2024-04-01', 61000.00, 7200.00, 2400.00, 59800.00, NOW(), 'admin'),
('EMP010', '2024-05-01', 62000.00, 7500.00, 2500.00, 59500.00, NOW(), 'admin');