from time import timezone
from dashboard.models import Goal
from django.shortcuts import get_object_or_404, redirect, render
import datetime 
from dashboard.my_calendar import CustomCal
from users.models import LoginDate, MyUser


def dashboard(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    if request.method == 'POST':
        if (request.POST['date_input'] == ''):
            Goal.objects.create(text=request.POST['goal_input'], user = the_user)
        else:
            date = request.POST['date_input']
            Goal.objects.create(text=request.POST['goal_input'] , due_date=date, date_str=date, user = the_user)
        return redirect(f'/dashboard/{pk}/')
    
    goals = Goal.objects.filter(completed=False, user=the_user)

    # create calendar for all months user has logged in 
    cals = CustomCal.calendar_list(pk)
    
    return render(request, 'dashboard/base_dashboard.html',{'goals':goals, 'cals':cals, 'user':the_user})


def goal_tick(request, user_pk, goal_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    goal = get_object_or_404(Goal, user = the_user, pk = goal_pk)
    goal.completed = True
    goal.save()
    return redirect(f'/dashboard/{user_pk}/')

def goal_edit(request, user_pk, goal_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    goal = get_object_or_404(Goal, user = the_user, pk = goal_pk)
    if (goal.editing == False):
        goal.editing = True
        goal.save()
        goals = Goal.objects.filter(completed=False, user = the_user)
        cals = CustomCal.calendar_list(user_pk)
        return render(request, 'dashboard/base_dashboard_edit.html',{'goals':goals, 'cals':cals})
    else:
        goal.editing = False
        goal.text = request.POST.get('goal_cell_edit', goal.text)
        if (request.POST.get('date_cell_edit', '') != ''):
            goal.due_date = request.POST.get('date_cell_edit', goal.due_date)
            goal.date_str = request.POST.get('date_cell_edit', goal.date_str)
        goal.save()
        return redirect(f'/dashboard/{user_pk}/')