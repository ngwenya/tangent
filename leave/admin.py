from django.contrib import admin
from .models import Leave, Employee


class LeaveAdmin(admin.ModelAdmin):

    list_display = ['start_date', 'end_date', 'leave_days']


class EmployeeAdmin(admin.ModelAdmin):

    list_display = ['start_date', 'leave', 'leave_days']

admin.site.register(Leave, LeaveAdmin)
admin.site.register(Employee, EmployeeAdmin)
