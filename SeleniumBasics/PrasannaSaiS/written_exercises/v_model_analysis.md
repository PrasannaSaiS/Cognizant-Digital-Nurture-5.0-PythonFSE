# Hands-On 2
# SDLC vs TDLC – V-Model & Agile QA Integration

**Name:** Mohammed Thoufik

**Track:** Python Full Stack Engineer

---

# Task 1: V-Model Mapping

## 1. V-Model Diagram

```
                 SDLC                           TDLC

 Requirements -----------------------> Acceptance Testing

 System Design ----------------------> System Testing

 Architecture Design ----------------> Integration Testing

 Module Design ----------------------> Unit Testing

                 Coding
```

The V-Model establishes a direct relationship between each development phase and its corresponding testing phase. Testing activities are planned alongside development rather than after development is complete.

---

## 2. SDLC Phase → Corresponding Test Artifact

| SDLC Phase | TDLC Phase | Test Artifact Produced |
|------------|------------|------------------------|
| Requirements | Acceptance Testing | Acceptance Test Plan |
| System Design | System Testing | System Test Cases |
| Architecture Design | Integration Testing | Integration Test Plan |
| Module Design | Unit Testing | Unit Test Cases |
| Coding | Test Execution | Source Code & Executable Build |

---

## 3. Entry and Exit Criteria

### Unit Testing

**Entry Criteria**

- Module development completed
- Source code compiled successfully
- Unit test cases prepared

**Exit Criteria**

- All unit test cases executed
- Critical defects fixed
- Required code coverage achieved

---

### Integration Testing

**Entry Criteria**

- Unit testing completed
- Modules integrated
- Integration test cases prepared

**Exit Criteria**

- Module communication verified
- Integration defects resolved
- No major interface issues

---

### System Testing

**Entry Criteria**

- Complete application available
- System test cases approved
- Test environment ready

**Exit Criteria**

- Functional testing completed
- No Critical or High severity defects
- Application meets business requirements

---

### Acceptance Testing

**Entry Criteria**

- System testing completed
- Stable build available
- Client acceptance criteria defined

**Exit Criteria**

- Client approves application
- Business requirements satisfied
- Product ready for deployment

---

## 4. Early QA Engagement Points

### Requirements Review

QA reviews the requirements to identify ambiguity, missing validations, and testability before development begins.

### Design Review

QA reviews the API design, database schema, and workflows to identify potential issues before coding starts.

---

# Task 2: Agile QA and Shift-Left Testing

## 5. Problems in Waterfall Testing

### Problem 1

Defects are discovered very late, making them more expensive to fix.

### Problem 2

Requirement misunderstandings remain unnoticed until testing begins.

### Problem 3

Large numbers of defects appear together near project completion, delaying delivery.

---

## 6. QA Responsibilities in Agile

### Sprint Planning

- Review user stories
- Define acceptance criteria
- Estimate testing effort

---

### Daily Stand-up

- Report testing progress
- Discuss blockers
- Coordinate with developers

---

### Sprint Review

- Validate completed features
- Demonstrate tested functionality
- Verify acceptance criteria

---

### Sprint Retrospective

- Discuss testing improvements
- Identify process gaps
- Suggest automation opportunities

---

## 7. Shift-Left Testing Practices

### a) Requirement Review

QA reviews requirements early to ensure they are complete, clear, and testable.

---

### b) Test Case Design Before Coding (TDD/BDD)

Test scenarios are prepared before implementation so developers clearly understand expected behavior.

---

### c) Static Code Analysis

Code quality tools detect coding issues, security vulnerabilities, and style violations before execution.

---

### d) API Contract Testing

API request and response formats are validated before integrating frontend and backend services.

---

# 8. Acceptance Criteria (Given-When-Then)

## Scenario 1 – Successful Course Creation

**Given**

The administrator is logged in.

**When**

Valid course details are submitted.

**Then**

The course is created successfully and HTTP 201 is returned.

---

## Scenario 2 – Duplicate Course Code

**Given**

A course with code "CS101" already exists.

**When**

The administrator submits another course using "CS101".

**Then**

The API returns an error indicating the course code already exists.

---

## Scenario 3 – Missing Required Fields

**Given**

The administrator opens the Create Course page.

**When**

The course name is left empty and the request is submitted.

**Then**

The API returns HTTP 422 validation errors and the course is not created.

---

# Conclusion

The V-Model ensures every development phase has a corresponding testing phase, improving software quality through early planning. Agile and Shift-Left testing further enhance quality by involving QA throughout development, reducing defects and delivery time.