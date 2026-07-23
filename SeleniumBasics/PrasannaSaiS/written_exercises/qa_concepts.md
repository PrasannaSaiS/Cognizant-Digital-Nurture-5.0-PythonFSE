# Hands-On 1
# QA Concepts, Functional Testing & Defect Lifecycle

**Name:** Mohammed Thoufik

**Track:** Python Full Stack Engineer

---

# Task 1: Map Testing Types to the Course Management API

## 1. Testing Levels

### Unit Testing
**Description:**
Tests a single function independently.

**Example:**
Verify that the `create_course()` function correctly creates a new course object when valid input is provided.

**Testing Type:** Functional Testing

---

### Integration Testing

**Description:**
Tests communication between two or more components.

**Example:**
Verify that the POST `/api/courses/` endpoint successfully stores a course in the database and returns HTTP 201.

**Testing Type:** Functional Testing

---

### System Testing

**Description:**
Tests the complete application from start to finish.

**Example:**
Create a course using the API, retrieve it using GET, update it using PUT, and finally delete it using DELETE.

**Testing Type:** Functional Testing

---

### User Acceptance Testing (UAT)

**Description:**
Performed from the end user's perspective.

**Example:**
A college administrator successfully creates a new course, verifies it appears in the course list, and confirms students can enroll.

**Testing Type:** Functional Testing

---

## 2. Functional vs Non-Functional Testing

### Functional Testing

Checks whether the application performs the expected functions correctly.

Example:
- Create Course
- Update Course
- Delete Course
- Retrieve Course

### Non-Functional Testing

Checks how well the application performs.

Example:

**Performance Test**

Verify that the Course Management API responds within **2 seconds** while handling **100 concurrent requests**.

---

## 3. Black Box vs White Box Testing

| Black Box Testing | White Box Testing |
|-------------------|------------------|
| Internal code is unknown | Internal code is known |
| Tests inputs and outputs | Tests program logic |
| Performed mainly by QA Engineers | Performed mainly by Developers |
| No programming knowledge required | Programming knowledge required |

**QA Tester:** Mostly performs Black Box Testing.

**Developer:** Mostly performs White Box Testing.

---

## 4. Formal Test Cases

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|--------------|-------------|---------------|------------|-----------------|---------------|-----------|
| TC001 | Create a course with valid details | API is running | Send POST request with valid course data | Course created successfully with HTTP 201 | | |
| TC002 | Create course with missing required field | API is running | Send POST request without course name | HTTP 422 validation error displayed | | |
| TC003 | Create duplicate course | Course already exists | Send POST request using existing course code | Duplicate course error returned | | |

---

# Task 2: Defect Lifecycle & Severity Classification

## 5. Defect Lifecycle

```
New
 ↓
Assigned
 ↓
Open
 ↓
Fixed
 ↓
Retest
 ↓
Verified
 ↓
Closed
```

### Rejected

The reported issue is not considered a defect or cannot be reproduced.

### Deferred

The defect is accepted but postponed for a future release because of low business priority.

---

## 6. Severity and Priority Classification

### Bug A

**Issue:**
POST `/api/courses/` returns HTTP 500 for every request.

**Severity:** Critical

**Priority:** P1

**Reason:**
The core functionality is completely broken.

---

### Bug B

**Issue:**
Course names longer than 150 characters are silently truncated.

**Severity:** Medium

**Priority:** P2

**Reason:**
Data integrity is affected but the application still works.

---

### Bug C

**Issue:**
Swagger documentation contains a spelling mistake.

**Severity:** Low

**Priority:** P4

**Reason:**
Only a cosmetic issue.

---

### Bug D

**Issue:**
Correct login occasionally returns HTTP 401 on the first attempt.

**Severity:** High

**Priority:** P1

**Reason:**
Intermittent authentication failures reduce system reliability and affect users.

---

## 7. Sample Defect Report

| Field | Value |
|-------|-------|
| Defect ID | BUG-001 |
| Title | POST /api/courses/ returns HTTP 500 |
| Environment | Windows 11, Chrome Latest |
| Build Version | v1.0 |
| Severity | Critical |
| Priority | P1 |
| Steps to Reproduce | 1. Open Swagger UI 2. Execute POST /api/courses/ with valid data |
| Expected Result | Course should be created successfully with HTTP 201 |
| Actual Result | HTTP 500 Internal Server Error returned |
| Attachments | Screenshot of HTTP 500 error |

---

## 8. Difference Between Severity and Priority

### Severity

Severity measures **how seriously a defect affects the system.**

### Priority

Priority measures **how quickly the defect should be fixed.**

### Example

A spelling mistake on the CEO's dashboard has:

- Severity: Low
- Priority: High

Reason:
Although the bug does not affect functionality, it is highly visible and should be fixed immediately.

---