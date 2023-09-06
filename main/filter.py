from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


def date_make(d):
    ymd = "%Y-%m-%d"
    dt = datetime(2021, 12, 31)
    if not isinstance(d, type(dt)):
        return datetime.strptime(d, ymd)
    else:
        return d
    

def sdt(dt):
    dt = date_make(dt)
    wd = dt.weekday()
    if wd == 6:
        return 1
    else:
        return wd*(-1)


def edt(dt):
    dt = date_make(dt)
    d_nextmonth = dt + relativedelta(months=1)
    edt = (d_nextmonth - timedelta(1)).day + 1
    return edt


def month(dt):
    dt = date_make(dt)
    return dt.month


def check(year, month, day, day_list):
    for i in day_list:
        if (year == i.year) and (month == i.month) and (day == i.day):
            return True
    return False


'''
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from main import app

def date_make(d):
    ymd = "%Y-%m-%d"
    dt = datetime(2021, 12, 31)
    if not isinstance(d, type(dt)):
        return datetime.strptime(d, ymd)
    else:
        return d
    

@app.template_filter('sdt')
def sdt(dt):
    dt = date_make(dt)
    wd = dt.weekday()
    if wd == 6:
        return 1
    else:
        return wd*(-1)

@app.template_filter('edt')
def edt(dt):
    dt = date_make(dt)
    d_nextmonth = dt + relativedelta(months=1)
    edt = (d_nextmonth - timedelta(1)).day + 1
    return edt

@app.template_filter('month')
def month(dt):
    dt = date_make(dt)
    return dt.month

@app.template_filter('check')
def check(year, month, day, day_list):
    for i in day_list:
        if (year == i.year) and (month == i.month) and (day == i.day):
            return True
    return False
'''