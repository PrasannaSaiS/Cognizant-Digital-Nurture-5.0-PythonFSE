-- Task 1: Subqueries

-- Step 35: Find all students enrolled in more courses than the average number of enrollments per student
SELECT s.student_id, s.first_name, s.last_name, COUNT(e.enrollment_id) AS enrollment_count
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.enrollment_id) > (
    SELECT AVG(student_enrollment_count) 
    FROM (
        SELECT COUNT(*) AS student_enrollment_count 
        FROM enrollments 
        GROUP BY student_id
    ) AS avg_subquery
);

-- Step 36: List courses in which all enrolled students have received a grade of 'A'
SELECT c.course_id, c.course_name, c.course_code
FROM courses c
WHERE EXISTS (
    SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id
) AND NOT EXISTS (
    SELECT 1 
    FROM enrollments e 
    WHERE e.course_id = c.course_id AND (e.grade != 'A' OR e.grade IS NULL)
);

-- Step 37: Find the professor with the highest salary in each department using a correlated subquery
SELECT p1.professor_id, p1.prof_name, p1.department_id, p1.salary
FROM professors p1
WHERE p1.salary = (
    SELECT MAX(p2.salary) 
    FROM professors p2 
    WHERE p2.department_id = p1.department_id
);

-- Step 38: Use a subquery in the FROM clause to calculate per-department average salary and filter above 85,000
SELECT dept_salaries.department_id, d.dept_name, ROUND(dept_salaries.avg_salary, 2) AS average_salary
FROM (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) AS dept_salaries
JOIN departments d ON dept_salaries.department_id = d.department_id
WHERE dept_salaries.avg_salary > 85000.00;


-- Task 2: Creating and Using Views

-- Step 39: Create a view for student enrollment summary with calculated GPA scales
CREATE VIEW vw_student_enrollment_summary AS
SELECT 
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name,
    COUNT(e.enrollment_id) AS courses_enrolled,
    AVG(CASE 
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'D' THEN 1
        WHEN e.grade = 'F' THEN 0
        ELSE NULL
    END) AS gpa
FROM students s
LEFT JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

-- Step 40: Create a view for course performance statistics
CREATE VIEW vw_course_stats AS
SELECT 
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    AVG(CASE 
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'D' THEN 1
        WHEN e.grade = 'F' THEN 0
        ELSE NULL
    END) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Step 41: Query the summary view to find high-performing students
SELECT * FROM vw_student_enrollment_summary 
WHERE gpa > 3.0;

-- Step 42: Attempt a write operation through a complex view modification rule
/* Execution Note: The following query will fail if run directly.
UPDATE vw_student_enrollment_summary
SET courses_enrolled = 5
WHERE full_name = 'Arjun Mehta';
*/

/* Analysis of Multi-Table View Modifiability:
Multi-table views that contain complex aggregates (like COUNT or AVG) and standard table JOINs 
are not inherently updatable by the database engine. Because a single row inside the view represents 
an evaluated synthesis of multiple logical records across distinct source locations, the relational engine 
cannot uniquely determine how to distribute updates back down to individual table entities without ambiguity.
*/

-- Step 43: Wipe and recreate a simplified view structure deploying a check option constraint
DROP VIEW IF EXISTS vw_course_stats;
DROP VIEW IF EXISTS vw_student_enrollment_summary;

CREATE VIEW vw_student_enrollment_summary AS
SELECT student_id, first_name, last_name, email, enrollment_year
FROM students
WHERE enrollment_year >= 2022
WITH CHECK OPTION;


-- Task 3: Stored Procedures and Transactions

-- Step 44: Create an verification handling enrollment function
CREATE OR REPLACE FUNCTION fn_enroll_student(
    p_student_id INT, 
    p_course_id INT, 
    p_enrollment_date DATE
) 
RETURNS VOID AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM enrollments 
        WHERE student_id = p_student_id AND course_id = p_course_id
    ) THEN
        RAISE EXCEPTION 'Enrollment Denied: Student % already registered for course %.', p_student_id, p_course_id;
    END IF;

    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (p_student_id, p_course_id, p_enrollment_date, NULL);
END;
$$ LANGUAGE plpgsql;

-- Step 45: Prepare log dependencies and implement the dynamic transfer procedure
CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id SERIAL PRIMARY KEY,
    student_id INT,
    old_department_id INT,
    new_department_id INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE PROCEDURE sp_transfer_student(
    p_student_id INT,
    p_new_dept_id INT
) AS $$
DECLARE
    v_old_dept_id INT;
BEGIN
    SELECT department_id INTO v_old_dept_id FROM students WHERE student_id = p_student_id;
    
    UPDATE students 
    SET department_id = p_new_dept_id 
    WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log (student_id, old_department_id, new_department_id)
    VALUES (p_student_id, v_old_dept_id, p_new_dept_id);
END;
$$ LANGUAGE plpgsql;

-- Step 46: Test transaction rollbacks under invalid structural inputs
/* Execution Note: Calling this procedure with an invalid department id (e.g., 99) 
will break the foreign key rule on 'students', forcing a rollback of the whole transaction block.
CALL sp_transfer_student(1, 99); 
*/

-- Step 47: Execute sub-transaction processing utilizing checkpoint operations
BEGIN;

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
VALUES (1, 4, '2026-06-16', NULL);

SAVEPOINT first_enrollment_saved;

-- Intentional failure execution using an invalid student ID link target
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
VALUES (999, 1, '2026-06-16', NULL);

-- Fallback mechanism handling partial errors:
-- ROLLBACK TO SAVEPOINT first_enrollment_saved;
-- COMMIT;
