from django.contrib import admin
from .models import Leave, Employee,  Period


class LeaveAdmin(admin.ModelAdmin):

    list_display = ['start_date', 'end_date', 'leave_days']


class EmployeeAdmin(admin.ModelAdmin):

    list_display = ['start_date', 'leave_days']


class PeriodsAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'period']


admin.site.register(Leave, LeaveAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Period, PeriodsAdmin)
