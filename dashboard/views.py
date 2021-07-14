from dashboard.models import Goals
from django.shortcuts import redirect, render
import datetime 
from calendar import HTMLCalendar
from dashboard.my_calendar import CustomCal


def dashboard(request):
    if request.method == 'POST':
        Goals.objects.create(text=request.POST['goal_input'], due_date=request.POST['date_input'])
        return redirect('dashboard')
    goals = Goals.objects.all()
    today = datetime.datetime.today()
    cal = CustomCal().formatmonth(today.year, today.month)
    return render(request, 'dashboard/dashboard.html',{'goals':goals, 'cal':cal})

