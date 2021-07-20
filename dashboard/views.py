from dashboard.models import Goal
from django.shortcuts import get_object_or_404, redirect, render
import datetime 
from calendar import HTMLCalendar
from dashboard.my_calendar import CustomCal
from bs4 import BeautifulSoup

def dashboard(request):
    invalid_entry = False
    if request.method == 'POST':
        if (request.POST['goal_input'] == '' and request.POST['date_input'] == ''):
            invalid_entry = True
        elif (request.POST['date_input'] == ''):
            Goal.objects.create(text=request.POST['goal_input'])
        else:
            Goal.objects.create(text=request.POST['goal_input'] , due_date=request.POST['date_input'])
    
    goals = Goal.objects.filter(completed=False)
    today = datetime.datetime.today()
    cal = CustomCal().formatmonth(today.year, today.month)
    return render(request, 'dashboard/base_dashboard.html',{'goals':goals, 'cal':cal, 'invalid_entry':invalid_entry})

def goal_tick(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    goal.completed = True
    goal.save()
    return redirect('dashboard')

def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if (goal.editing == False):
        goal.editing = True
        goal.save()
        goals = Goal.objects.filter(completed=False)
        today = datetime.datetime.today()
        cal = CustomCal().formatmonth(today.year, today.month)
        return render(request, 'dashboard/base_dashboard_edit.html',{'goals':goals, 'cal':cal})
    else:
        goal.editing = False
        goal.text = request.POST.get('goal_cell_edit', goal.text)
        if (request.POST.get('date_cell_edit', '') != ''):
            goal.due_date = request.POST.get('date_cell_edit', goal.due_date)
        goal.save()
        return redirect('dashboard')