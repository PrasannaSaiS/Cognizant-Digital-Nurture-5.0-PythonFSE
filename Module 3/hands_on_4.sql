-- Task 1: Baseline Performance — No Indexes

-- Step 48: Baseline execution plan inspection
EXPLAIN 
SELECT s.first_name, s.last_name, c.course_name 
FROM enrollments e 
JOIN students s ON s.student_id = e.student_id 
JOIN courses c ON c.course_id = e.course_id 
WHERE s.enrollment_year = 2022;

/* Steps 49 & 50: Plan Observations
- Displays Sequential Scan (Seq Scan) across all tables (students, enrollments, courses)[cite: 799].
- High cost estimate because the database engine must scan every row to resolve the WHERE clause[cite: 803].
*/


-- Task 2: Add Indexes and Compare Plans

-- Step 51: Create B-Tree index on the filtering column
CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);

-- Step 52: Create composite UNIQUE index to speed up joins and block duplicates
CREATE UNIQUE INDEX idx_enrollments_student_course ON enrollments(student_id, course_id);

-- Step 53: Create index on alphanumeric lookup column
CREATE INDEX idx_courses_course_code ON courses(course_code);

-- Step 54: Re-verify optimization path changes
EXPLAIN 
SELECT s.first_name, s.last_name, c.course_name 
FROM enrollments e 
JOIN students s ON s.student_id = e.student_id 
JOIN courses c ON c.course_id = e.course_id 
WHERE s.enrollment_year = 2022;

/*
Plan Analysis:
- Shifting from 'Seq Scan' to 'Index Scan' on indexed constraints[cite: 808].
- Lower estimated query cost owing to instant pointer lookups.
*/

-- Step 55: Create a partial index targeting unevaluated enrollment records
CREATE INDEX idx_enrollments_pending_grade 
ON enrollments(student_id) 
WHERE grade IS NULL;


-- Task 3: Identify and Fix the N+1 Problem

/*
Step 56: Conceptual N+1 Performance Loop Pattern (Python Pseudocode)

# Anti-pattern: Generates 1 query initially, plus N secondary row queries
enrollments = db.execute("SELECT * FROM enrollments")
for row in enrollments:
    student = db.execute("SELECT first_name, last_name FROM students WHERE student_id = %s", row['student_id'])
    
Total Query Count: 1 + N (Translates to 13 total queries with current sample data)
*/

-- Step 57: Optimized single-query replacement (Eager Loading)
SELECT e.enrollment_id, e.enrollment_date, e.grade, s.first_name, s.last_name 
FROM enrollments e
JOIN students s ON e.student_id = s.student_id;

/*
Steps 58 & 59: Round-Trip and Scale Metrics
- Performance Impact: Restricts database communication down to 1 single network transaction[cite: 821].
- 10,000 Row Scale Test: A standard N+1 application footprint triggers 10,001 database queries 
  (1 primary fetch + 10,000 isolated child records requests)[cite: 818, 819]. The JOIN rewrite runs exactly 1 query total[cite: 820, 821].
*/
