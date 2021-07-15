from dashboard.models import Goal
from django.shortcuts import get_object_or_404, redirect, render
import datetime 
from calendar import HTMLCalendar
from dashboard.my_calendar import CustomCal


def dashboard(request):
    if request.method == 'POST':
        Goal.objects.create(text=request.POST['goal_input'], due_date=request.POST['date_input'])
        return redirect('dashboard')
    
    goals = Goal.objects.filter(completed=False)
    today = datetime.datetime.today()
    cal = CustomCal().formatmonth(today.year, today.month)
    return render(request, 'dashboard/dashboard.html',{'goals':goals, 'cal':cal})

def goal_tick(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    goal.completed = True
    goal.save()
    return redirect('dashboard')

