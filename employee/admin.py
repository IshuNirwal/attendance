from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class EmployeeAdmin(BaseUserAdmin):
    list_display = ('id', 'name', 'email', 'role', 'employee_id')
    search_fields = ('name', 'email', 'employee_id')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'role', 'employee_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'employee_id', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    filter_horizontal=()

admin.site.register(Employee, EmployeeAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'arrivaltime', 'departuretime','is_present']

admin.site.register(Attendance, AttendanceAdmin)