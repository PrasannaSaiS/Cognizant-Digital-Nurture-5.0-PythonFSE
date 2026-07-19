from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = router.urls
