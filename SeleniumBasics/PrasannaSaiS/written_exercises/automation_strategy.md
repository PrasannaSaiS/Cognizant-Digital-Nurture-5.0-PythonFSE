# Hands-On 3
# Test Automation Process, Lifecycle & Framework Types

**Name:** Mohammed Thoufik

**Track:** Python Full Stack Engineer

---

# Task 1: Automation Decision and Test Case Selection

## 1. Criteria for Deciding Whether to Automate a Test Case

### Criterion 1 – Repeatability

Tests executed frequently are good candidates for automation.

**Application:**
The POST `/api/courses/` endpoint is executed repeatedly during regression testing, making it suitable for automation.

---

### Criterion 2 – Stability

Stable functionality with infrequent UI or API changes is easier to automate.

**Application:**
The course creation API is stable and follows REST standards, making automation reliable.

---

### Criterion 3 – Time Consumption

Manual execution of repetitive tests consumes significant time.

**Application:**
Automating course creation saves time during every regression cycle.

---

### Criterion 4 – Business Criticality

Critical business functionality should always be automated.

**Application:**
Creating courses is a core feature of the Course Management API, so automation is highly recommended.

---

### Criterion 5 – Reusability

Automated test scripts should be reusable across multiple releases.

**Application:**
The same POST endpoint validation can be reused whenever the API is updated.

---

## 2. Automate or Manual?

| Test Case | Decision | Justification |
|-----------|----------|---------------|
| Regression test for all CRUD endpoints after every code change | **Automate** | Executed repeatedly after every build. |
| Exploratory testing of a new search feature | **Manual** | Requires human creativity and investigation. |
| Performance test with 100 concurrent GET requests | **Automate** | Load testing tools can execute concurrent requests consistently. |
| UI test for the login form | **Automate** | Frequently executed and suitable for Selenium. |
| Verify Swagger API documentation accuracy | **Manual** | Mostly requires human review of descriptions and documentation. |
| Smoke test to verify API availability after deployment | **Automate** | Quick health check performed after every deployment. |

---

## 3. Test Automation ROI

**Definition**

Automation ROI (Return on Investment) measures whether the time, cost, and effort spent creating automation provide long-term benefits compared to manual testing.

### Benefits

- Faster regression testing
- Higher test coverage
- Reduced manual effort
- Early defect detection
- Repeatable and reliable execution

### Costs

- Script development
- Maintenance
- Tool setup
- Training
- Infrastructure

Automation delivers positive ROI when the long-term savings exceed the initial investment.

---

# Task 2: Automation Test Lifecycle & Framework Selection

## 4. Automation Test Lifecycle

```
Requirement Analysis
        ↓
Feasibility Analysis
        ↓
Tool Selection
        ↓
Framework Design
        ↓
Test Script Development
        ↓
Test Execution
        ↓
Result Analysis
        ↓
Maintenance
```

### Phase Description

**Requirement Analysis**
Identify automation candidates.

**Feasibility Analysis**
Determine whether automation is technically and economically feasible.

**Tool Selection**
Select tools such as Selenium, pytest, and WebDriver Manager.

**Framework Design**
Choose an automation framework structure.

**Test Script Development**
Develop reusable automation scripts.

**Test Execution**
Run automated tests and collect results.

**Result Analysis**
Analyze failures and generate reports.

**Maintenance**
Update automation scripts whenever the application changes.

---

## 5. Automation Framework Types

| Framework | Description | Advantages | Disadvantages |
|-----------|-------------|------------|---------------|
| Linear | Scripts executed sequentially. | Easy to learn. | Difficult to maintain. |
| Modular | Application divided into reusable modules. | Better code reuse. | Initial design effort required. |
| Data-Driven | Test data separated from scripts. | Easy to test multiple inputs. | Slightly more complex. |
| Keyword-Driven | Uses keywords to define test steps. | Non-programmers can contribute. | Requires framework setup. |
| Hybrid | Combines multiple framework approaches. | Flexible, scalable, maintainable. | Higher initial complexity. |

---

## 6. Recommended Framework for the Course Management API

**Recommended Framework: Hybrid Framework**

### Reasons

- Supports reusable modules.
- Allows data-driven API testing.
- Easy to integrate with Selenium and pytest.
- Scalable for future automation.
- Easier maintenance for large projects.

---

## 7. Automation Risks and Limitations

### Risk 1

Frequent UI changes increase maintenance effort.

---

### Risk 2

Poorly designed locators can make Selenium tests unstable.

---

### Risk 3

Automation cannot completely replace exploratory and usability testing.

---

## 8. Conclusion

Automation should focus on repetitive, stable, and business-critical functionality. A Hybrid Framework provides the best balance between maintainability, scalability, and reusability for the Course Management API. Proper planning, framework selection, and regular maintenance ensure long-term automation success and a positive return on investment.