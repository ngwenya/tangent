# Stdlib imports
from threading import Timer
from time import sleep
from datetime import datetime, timedelta

# my app imports
from leave.models import Employee, Period


def manage_new_periods():
    """
    this method runs through the employees and search for those who's period is None. Which means the specific employee
    has not period created for them since start date The default is 0.
    A new period is then created and is a year apart from the start date
    The start date is extracted from the employee start date
    A period is calculated based on 365 days
    :param request:
    :return:
    """
    employee_list = Employee.objects.filter(periods=None)
    for employee in employee_list:
        end_of_period = employee.start_date + timedelta(12 * 365 / 12)   # future date periods since start start date
        new_period = Period(
            start_date=employee.start_date,
            end_date=end_of_period,
            period=1
        )
        new_period.save()
        employee.periods.add(new_period)  # add period to a specific employee


def manage_existing_periods():
    """
    this method is the entry point of the scheduler.
    It check loads every employee to a list and then call a method that calculates and returns True if its the end of
    period since the start of the current period. It passes the start and end date values to this method.
    It check period returns True, it then processed to update leave days,then create a new period with a date that lies
    in future (following day)
    :return:
    """
    periods = Period.objects.select_related().values('employee__id', 'start_date', 'end_date', 'period')
    for period in periods:
        end = period['end_date']
        employee = period['employee__id']
        employee_period = period['period']
        if check_period(end) is True:  # if a new period is due then update leave days and create a new period
            update_leave_days(employee)
            create_new_period(employee, employee_period)


def create_new_period(employee, period):
    """
    This method takes employee id and period number (indicating how many periods since they started working)
    a new period is created and the date start 24 hours ahead of time to ensure its a new cycle.
    a new period end date is the calculated based on the above
    new period number is incremented from the current period
    :param employee:
    :param period:
    :return:
    """
    today = datetime.today().date()
    new_period = period + 1
    new_start = today + timedelta(hours=24)  # new period starts in a days time
    end_of_period = new_start + timedelta(12 * 365 / 12)  # future date periods since start date (above) 365 days diff
    Period.objects.filter(employee__id=employee).update(  # object is updated with new records
        start_date=new_start,
        end_date=end_of_period,
        period=new_period
    )


def update_leave_days(employee):
    """
    Employee leave days are updated
    If there is any remainder of days from current period, these are then added the new period / cycle
    The days to be carried over are limited to 5 and a new cycle leave days is 18
    :param employee:
    :return:
    """
    annual_leave = 18
    max_carry = 5
    employees = Employee.objects.filter(id=employee).values()
    employee = [em for em in employees]
    max_carried = range(1, 6)  # max number of days to be carried to new cycle
    if employee[0]['leave_days'] in max_carried:
        carried = employee[0]['leave_days']  # if the days are within the range, then the current days are usd
        employees.update(
            leave_days=carried+annual_leave
        )
    else:
        carried = max_carry  # if the remaining days are beyond the range, then 5 is used as maximum
        employees.update(  # update object
            leave_days=carried + annual_leave
        )
    return carried


def check_period(end):
    """
    method that accepts the employee period end date as an argument and checks it against today's date.
    if they are equal then it means the period ends today or not and return  true or false respectively
    :param end:
    :return:
    """
    if end == datetime.today().date():
        end_of_period = True
    else:
        end_of_period = False

    return end_of_period


class RepeatedTimer(object):
    """
    Timer class using threading to manage the repeated events.
    This class has 3 methods which control how the function that is being called run.
    It accepts the function name, which it calls repeatedly according the intervals passed to it
    """

    def __init__(self, interval, function, *args, **kwargs):
        """
        constructor method which fires the start method
        :param interval:
        :param function:
        :param args:
        :param kwargs:
        """
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        """
        this is called from the start method run the function which is to be scheduled. It is invoked by being passed
        to the Timer class which takes the interval and function name which in this case is contained in ths method
        :return:
        """
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        """
        a check is performed to ensure the function is not already started then it is started
        :return:
        """
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


task_existing_periods = RepeatedTimer(86400, manage_existing_periods)  # run once a day
task_new_periods = RepeatedTimer(43200, manage_new_periods)  # run once half way through a day
