-- Task 1: Insert, Update and Delete Data

-- Step 15: Insert the provided sample data into all five tables
INSERT INTO departments (dept_name, hod_name, budget) VALUES
('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
('Electronics', 'Dr. Priya Nair', 620000.00),
('Mechanical', 'Dr. Suresh Iyer', 540000.00),
('Civil', 'Dr. Ananya Sharma', 430000.00);

INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Arjun', 'Mehta', 'arjun.mehta@college.edu', '2003-04-12', 1, 2022),
('Priya', 'Suresh', 'priya.suresh@college.edu', '2003-07-25', 1, 2022),
('Rohan', 'Verma', 'rohan.verma@college.edu', '2002-11-08', 2, 2021),
('Sneha', 'Patel', 'sneha.patel@college.edu', '2004-01-30', 3, 2023),
('Vikram', 'Das', 'vikram.das@college.edu', '2003-09-14', 1, 2022),
('Kavya', 'Menon', 'kavya.menon@college.edu', '2002-05-17', 2, 2021),
('Aditya', 'Singh', 'aditya.singh@college.edu', '2004-03-22', 4, 2023),
('Deepika', 'Rao', 'deepika.rao@college.edu', '2003-08-09', 1, 2022);

INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
('Data Structures & Algorithms', 'CS101', 4, 1),
('Database Management Systems', 'CS102', 3, 1),
('Object Oriented Programming', 'CS103', 4, 1),
('Circuit Theory', 'EC101', 3, 2),
('Thermodynamics', 'ME101', 3, 3);

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
(1, 1, '2022-07-01', 'A'),
(1, 2, '2022-07-01', 'B'),
(2, 1, '2022-07-01', 'B'),
(2, 3, '2022-07-01', 'A'),
(3, 4, '2021-07-01', 'A'),
(4, 5, '2023-07-01', NULL),
(5, 1, '2022-07-01', 'C'),
(5, 2, '2022-07-01', 'A'),
(6, 4, '2021-07-01', 'B'),
(7, 5, '2023-07-01', NULL),
(8, 1, '2022-07-01', 'A'),
(8, 3, '2022-07-01', 'A');

INSERT INTO professors (prof_name, email, department_id, salary) VALUES
('Dr. Anand Krishnan', 'anand.k@college.edu', 1, 95000.00),
('Dr. Meena Pillai', 'meena.p@college.edu', 1, 88000.00),
('Dr. Sunil Rajan', 'sunil.r@college.edu', 2, 82000.00),
('Dr. Latha Gopal', 'latha.g@college.edu', 3, 79000.00),
('Dr. Kartik Bose', 'kartik.b@college.edu', 4, 76000.00);

-- Step 16: Insert two additional students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Amit', 'Sharma', 'amit.sharma@college.edu', '2003-11-23', 1, 2022),
('Riya', 'Sen', 'riya.sen@college.edu', '2004-02-14', 2, 2023);

-- Step 17: Update the grade of student_id = 5 for course_id = 1 from 'C' to 'B'
UPDATE enrollments 
SET grade = 'B' 
WHERE student_id = 5 AND course_id = 1;

-- Step 18: Delete enrollments where grade IS NULL
DELETE FROM enrollments 
WHERE grade IS NULL;

-- Step 19: Verify row counts
SELECT COUNT(*) AS total_students FROM students;
SELECT COUNT(*) AS total_enrollments FROM enrollments;


-- Task 2: Single-Table Queries and Filtering

-- Step 20: Retrieve all students enrolled in 2022, ordered by last_name alphabetically
SELECT * FROM students 
WHERE enrollment_year = 2022 
ORDER BY last_name ASC;

-- Step 21: Find all courses with more than 3 credits, sorted by credits descending
SELECT * FROM courses 
WHERE credits > 3 
ORDER BY credits DESC;

-- Step 22: List all professors whose salary is between 80,000 and 95,000
SELECT * FROM professors 
WHERE salary BETWEEN 80000.00 AND 95000.00;

-- Step 23: Find all students whose email ends with '@college.edu'
SELECT * FROM students 
WHERE email LIKE '%@college.edu';

-- Step 24: Count the total number of students per enrollment_year
SELECT enrollment_year, COUNT(*) AS student_count 
FROM students 
GROUP BY enrollment_year;


-- Task 3: Multi-Table Joins

-- Step 25: List each student's full name alongside the name of their department
SELECT CONCAT(s.first_name, ' ', s.last_name) AS full_name, d.dept_name 
FROM students s
JOIN departments d ON s.department_id = d.department_id;

-- Step 26: Show each enrollment along with the student's name and the course name
SELECT e.enrollment_id, s.first_name, s.last_name, c.course_name 
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;

-- Step 27: Find all students who are NOT enrolled in any course
SELECT s.* FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;

-- Step 28: Display every course along with the number of students enrolled in it (including 0)
SELECT c.course_name, COUNT(e.enrollment_id) AS student_count
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

-- Step 29: List each department along with its professors and salaries (including empty departments)
SELECT d.dept_name, p.prof_name, p.salary
FROM departments d
LEFT JOIN professors p ON d.department_id = p.department_id;


-- Task 4: Aggregations and Grouping

-- Step 30: Calculate the total number of enrollments per course
SELECT c.course_name, COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

-- Step 31: Find the average salary of professors per department rounded to 2 decimal places
SELECT d.dept_name, ROUND(AVG(p.salary), 2) AS average_salary
FROM departments d
JOIN professors p ON d.department_id = p.department_id
GROUP BY d.department_id, d.dept_name;

-- Step 32: Find all departments where the total budget exceeds 600,000
SELECT * FROM departments 
WHERE budget > 600000.00;

-- Step 33: Show the grade distribution for course CS101
SELECT grade, COUNT(*) AS grade_count
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY grade;

-- Step 34: List departments where more than 2 students are enrolled across all courses in that department
SELECT d.dept_name, COUNT(DISTINCT e.student_id) AS total_enrolled_students
FROM departments d
JOIN courses c ON d.department_id = c.department_id
JOIN enrollments e ON c.course_id = e.course_id
GROUP BY d.department_id, d.dept_name;
