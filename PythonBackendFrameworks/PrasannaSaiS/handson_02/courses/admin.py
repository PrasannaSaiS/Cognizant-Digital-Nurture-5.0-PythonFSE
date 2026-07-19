from django.contrib import admin
from .models import Department, Course, Student, Enrollment


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'department']
    search_fields = ['name', 'code']
    list_filter = ['department']


admin.site.register(Department)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
admin.site.register(Enrollment)
