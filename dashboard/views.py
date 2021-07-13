from django.shortcuts import render
import datetime 
from calendar import HTMLCalendar


def dashboard(request):
    today = datetime.datetime.today()
    cal = HTMLCalendar().formatmonth(today.year, today.month)
    return render(request, 'dashboard/dashboard.html',{'cal':cal})

