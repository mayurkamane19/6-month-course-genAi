CREATE DATABASE employee_management;
USE employee_management;

CREATE TABLE departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    dept_id INT,
    salary DECIMAL(10,2),
    join_date DATE,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

INSERT INTO departments (dept_name)
VALUES ('HR'), ('IT'), ('Finance'), ('Marketing');

INSERT INTO employees(emp_name, email, phone, dept_id, salary, join_date)
VALUES
('Rahul Sharma', 'rahul@gmail.com', '9988776655', 1, 40000, '2022-05-18'),
('Sneha Patil', 'sneha@gmail.com', '9988665544', 2, 55000, '2023-01-10'),
('Amit Verma', 'amit@gmail.com', '8877665544', 3, 50000, '2021-11-02'),
('Priya Singh', 'priya@gmail.com', '8899776655', 2, 65000, '2020-06-12'),
('Rohit Mehra', 'rohit@gmail.com', '7766554433', 1, 45000, '2023-02-05');


SELECT*FROM employees;


CREATE DATABASE student_management;
USE student_management;
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    course VARCHAR(50),
    marks INT
);
INSERT INTO students (name, email, phone, course, marks)
VALUES
('Rahul Sharma', 'rahul@gmail.com', '9988776655', 'Python', 85),
('Sneha Patil', 'sneha@gmail.com', '9988665544', 'Data Science', 92),
('Amit Verma', 'amit@gmail.com', '8877665544', 'Java', 78);
SELECT * FROM students;


SELECT*FROM student;