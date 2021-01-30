from django.contrib import admin
from .models import *

# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    manager = 'manager_id'
    list_display = ("EmpId","last_name", "first_name","role_id",manager,"Is_Active_Employee","dept_id")


admin.site.register(Employee,EmployeeAdmin)


class RolesAdmin(admin.ModelAdmin):
    list_display = ("role_id", "role","description")

admin.site.register(Roles,RolesAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("dept_id", "dept_name","Is_Active")
admin.site.register(Department,DepartmentAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ("rating_id", "grade","grade_description")
admin.site.register(Rating,RatingAdmin)


class AppraisalAdmin(admin.ModelAdmin):
    list_display = ("appraisal_id", "appraisal_date","app_supervisor_comments","dept_id","emp_id","rating_id")
admin.site.register(Appraisal,AppraisalAdmin)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ("mgr_id", "first_name","last_name")
admin.site.register(Manager,ManagerAdmin)