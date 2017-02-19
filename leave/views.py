# Stdlib imports
from datetime import datetime, timedelta

# Core Django imports
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from settings import base as settings
from django.utils.dateparse import parse_date
from django.http import JsonResponse

# My app imports
from .models import Leave, Employee
from .forms import LeaveRequestForm
from .forms import LoginForm


def login_view(request):
    """
    Handle log in. First authenticate the user and then log them in.
    The login url (which is the dashboard) is fined in the settings file
    :param request:
    :return:
    """
    template = 'leave/user_login.html',
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_URL)
        else:
            form = LoginForm()

    return render(request, template, {'login_form': form})


def logout_view(request):
    """
    log the user out and return to log in page
    :param request:
    :return:
    """
    logout(request)

    return redirect(settings.LOGOUT_REDIRECT_URL)


def dashboard(request):
    """
    This is the dashboard. It has the form for leave requests and the remaining number of leave days
    :param request:
    :return:
    """
    template = 'leave/dashboard.html'

    return render(request, template, {'leave_form': LeaveRequestForm()})


def leave_request(request):
    """
    Entry point for the leave request. This method performs minimal operation and passes specific functionality to
    other methods. It checks for the number of days since the employee started working. If they are is above 90 days
    (which I use to indicate 3 months) then it proceeds to the other functions. If not then the employer is notified of
    such.
    :param request:
    :return:
    """
    leave_start = request.POST['start_date']
    leave_end = request.POST['end_date']

    employee = Employee.objects.get(employee=request.user)
    work_start_date = employee.start_date
    min_period = calculate_min_period(work_start_date)
    if min_period > 90:  # check if employed for more than 3 months already
        # no of days applied for excluding weekends
        required_leave_days = calculate_req_leave_days(leave_start, leave_end)
        process_application(request, employee, required_leave_days, leave_start, leave_end)  # process the application

    else:
        return JsonResponse({
            'results': 'Failed'
        })


def process_application(request, employee, required_leave_days, leave_start, leave_end):
    """
    The leave request is processed here. If number of leave days available are greater or equal required leave days then
    the leave is created and employee remaining days are updated according to the difference
    :param request:
    :param employee:
    :param required_leave_days:
    :param leave_start:
    :param leave_end:
    :return:
    """
    if employee.leave_days >= required_leave_days:
        employee.leave_days -= required_leave_days
        create_leave(leave_start, leave_end, employee, required_leave_days)
        update_employee(request, employee.leave_days)

    else:
        decline_leave(leave_start, leave_end, employee, required_leave_days)
        update_employee(request, employee.leave_days)


def decline_leave(leave_start, leave_end, employee, required_leave_days):
    """
    A leave application is declined due to insufficient number of leave days remaining. This is performed when an
    employee requests more days than they have remaining.
    :param leave_start:
    :param leave_end:
    :param employee:
    :param required_leave_days:
    :return:
    """
    new_leave = Leave(
        start_date=leave_start,
        end_date=leave_end,
        leave_days=required_leave_days,
        status=3
    )
    new_leave.save()
    employee.leave.add(new_leave)


def update_employee(request, remaining_leave_days):
    """
    The employee records are updated by updating the remaining leave days. If the days have changed since the last time
    a new value is recorded others the old one is used.
    :param request:
    :param remaining_leave_days:
    :return:
    """
    Employee.objects.filter(employee=request.user).update(
        leave_days=remaining_leave_days
    )


def create_leave(start, end, employee, required_leave_days):
    """
    Leave is created and marked approved by adding a status valued of '2'. New leave is added to the employee
    :param start:
    :param end:
    :param employee:
    :param required_leave_days:
    :return:
    """
    new_leave = Leave(
        start_date=start,
        end_date=end,
        leave_days=required_leave_days,
        status=2
    )
    new_leave.save()
    employee.leave.add(new_leave)


def calculate_rem_leave_days(request, required_leave_days, employee):
    """
    calculates the remaining leave days for the employer by using the 'required leave days' value and the existing leave
    days. The difference is the remaining leave days
    :param request:
    :param required_leave_days:
    :param employee:
    :return:
    """
    if employee.leave_days >= required_leave_days:
        employee.leave_days -= required_leave_days
        return employee.leave_days
    else:
        return employee.leave_days


def calculate_req_leave_days(start, end):
    """
    works out the requested leave days by getting the difference between 2 dates and exclude weekends.
    :param start:
    :param end:
    :return:
    """
    new_start = parse_date(start)  # parse the date string to convert it into a Python datetime.date type
    new_end = parse_date(end)
    delta = timedelta(days=1)
    leave_days = 0
    weekend = {5, 6}  # a set to indicate Saturday and Sunday as weekend to be excluded
    while new_start <= new_end:
        if new_start.weekday() not in weekend:
            leave_days += 1
        new_start += delta
    return leave_days


def calculate_min_period(start_date):
    """
    calculates the date between start and today (and return an absolute value)
    to determine if the employee qualifies to apply.
    :param start_date:
    :return:
    """
    today = datetime.today().date()
    return abs((today-start_date).days)
