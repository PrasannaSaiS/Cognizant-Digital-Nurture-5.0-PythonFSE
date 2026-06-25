-- Task 1: Create the Database and Tables

-- 1. Create a new database named college_db
CREATE DATABASE college_db;

-- 2. Create the master departments table first to establish foreign key targets
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

-- 3. Create the students table referencing departments
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 4. Create the courses table referencing departments
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 5. Create the enrollments table as a bridge table linking students and courses
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- 6. Create the professors table referencing departments
CREATE TABLE professors (
    professor_id SERIAL PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);


-- Task 2: Verify Normalisation

/* 1NF (First Normal Form) Analysis:
The schema complies with 1NF because all columns hold atomic (indivisible) values. 
A violation would occur if multiple values, like storing multiple phone numbers 
separated by commas, were placed inside a single field instead of using a separate table.

2NF (Second Normal Form) Analysis:
The tables comply with 2NF because every non-key attribute is fully dependent on its 
table's primary key. In the enrollments table, while a composite business key exists 
(student_id + course_id), the surrogate single primary key (enrollment_id) ensures 
direct full functional dependency for every remaining non-key metric.

3NF (Third Normal Form) Analysis:
The schema satisfies 3NF because there are no transitive dependencies. Every non-key column 
depends directly on the primary key, and nothing else. Storing the dept_name directly in 
the students table would violate 3NF, because dept_name depends on department_id, which 
subsequently depends on the student_id. Keeping them isolated prevents data redundancy.
*/


-- Task 3: Alter and Extend the Schema

-- 10. Add a column phone_number VARCHAR(15) to the students table
ALTER TABLE students 
ADD COLUMN phone_number VARCHAR(15);

-- 11. Add a column max_seats INT DEFAULT 60 to the courses table
ALTER TABLE courses 
ADD COLUMN max_seats INT DEFAULT 60;

-- 12. Add a CHECK constraint to enrollments ensuring a valid grade structure or NULL
ALTER TABLE enrollments 
ADD CONSTRAINT chk_valid_grade 
CHECK (grade IN ('A', 'B', 'C', 'D', 'F') OR grade IS NULL);

-- 13. Rename the hod_name column in departments to head_of_dept
ALTER TABLE departments 
RENAME COLUMN hod_name TO head_of_dept;

-- 14. Drop the phone_number column to simulate a schema rollback
ALTER TABLE students 
DROP COLUMN phone_number;
