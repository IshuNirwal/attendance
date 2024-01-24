from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class EmployeeAdmin(UserAdmin):
    list_display = ('id', 'name', 'email', 'employee_id', 'role','barcode')
admin.site.register(Employee, EmployeeAdmin)
