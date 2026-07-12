This exercise book covers Python Backend Frameworks for the Digital Nurture 5.0 Deep Skilling
Program. The 10 hands-on exercises progressively build your backend development skills — starting
from web framework foundations and Django, moving through Flask and FastAPI, and culminating in
RESTful API design, authentication, and microservices architecture.
All exercises are built around a single scenario — a Course Management API — so each hands-on
adds a new capability to the same system.

Submission Guidelines
• Organise solutions in a folder named PythonBackendFrameworks/<YourName>/
• Each hands-on gets its own subfolder: handson_01/, handson_02/, ...
• Include a requirements.txt in each subfolder listing the packages used
• Push to your GitHub repository and share the URL with your POC
NOTE:
Hands-On 1–3 use Django. Hands-On 4–5 use Flask. Hands-On 6–7 use FastAPI. Hands-On
8–10 are framework-agnostic — implement in the framework of your choice.


Common Scenario: Course Management API
All exercises build one unified backend project — a Course Management API for a college system.
Each hands-on adds a new layer: starting from a simple Django project, then recreating key features in
Flask and FastAPI, and finally adding authentication and API design best practices.
 The Course Management API allows administrators to manage departments, courses, students, and
enrollments. It exposes RESTful endpoints consumed by a frontend application. You will build this
API three times — once each in Django, Flask, and FastAPI — to understand how each framework
approaches the same problem differently.
Core API Endpoints (implement across all frameworks)
Endpoint Method Resource Description
/api/courses/ GET Courses List all courses
/api/courses/ POST Courses Create a new course
/api/courses/{id}/ GET Courses Retrieve a course by ID
/api/courses/{id}/ PUT Courses Update a course
/api/courses/{id}/ DELETE Courses Delete a course
/api/students/ GET/POST Students List or create students
/api/enrollments/ POST Enrollments Enroll a student in a course
/api/auth/login/ POST Auth Login and receive JWT token

