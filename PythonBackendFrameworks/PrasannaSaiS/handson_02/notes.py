"""Notes for Hands-On 1: Django framework foundations.

1. Request-response cycle for GET /api/courses/:
   - The browser sends an HTTP GET request to /api/courses/.
   - Django's URL router matches the path to a view function or class.
   - The view processes the request, often querying a model to fetch data from the database.
   - The view builds an HttpResponse object and returns it to the browser.

2. Middleware in the cycle:
   - Middleware sits between the request entering Django and the response leaving it.
   - It can inspect or modify requests/responses globally.
   - Built-in examples:
       * AuthenticationMiddleware: attaches the authenticated user to the request.
       * SecurityMiddleware: adds security-related headers and enforces settings.

3. WSGI vs ASGI:
   - WSGI is the traditional synchronous request/response interface for Python web apps.
   - ASGI is the newer asynchronous interface that supports async views, long-lived connections, and WebSockets.
   - Django uses WSGI by default for its standard deployment stack.
   - You would switch to ASGI when building async-heavy applications or using WebSockets.

4. MVC vs Django MVT:
   - MVC: Model (data), View (UI/controller logic), Controller (handles input and flow).
   - Django MVT: Model (data layer), View (business logic/handler), Template (presentation layer).
   - In Django, the View plays the role of the Controller in MVC.
"""
