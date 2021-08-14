from dashboard.models import Goal
from django.shortcuts import get_object_or_404, redirect, render
import datetime 
from dashboard.my_calendar import CustomCal
from users.models import MyUser, LoginDate
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    invalid_entry = False
    if request.method == 'POST':
        if (request.POST['goal_input'] == '' and request.POST['date_input'] == ''):
            invalid_entry = True
        elif (request.POST['date_input'] == ''):
            Goal.objects.create(text=request.POST['goal_input'], user = the_user)
        else:
            Goal.objects.create(text=request.POST['goal_input'] , due_date=request.POST['date_input'], user = the_user)
    
    goals = Goal.objects.filter(completed=False, user=the_user)

    cal = colour_calendar(pk=pk)

    return render(request, 'dashboard/base_dashboard.html',{'goals':goals, 'cal':cal, 'invalid_entry':invalid_entry, 'user':the_user})

def colour_calendar(pk):
    # get user object that this dashboard is specific to
    the_user = MyUser.objects.get(pk=pk)
    last_login_date = datetime.datetime.date(the_user.last_login)

    # create login date object (for each time you login) IF there isn't one for that day already
    if(LoginDate.objects.filter(login_date=last_login_date).count() == 0):
        LoginDate.objects.create(user=the_user, login_date=last_login_date)

    today = datetime.datetime.today()
    cal = CustomCal().formatmonth(today.year, today.month)
    # give one colour to today's date and make it bold
    cal = cal.replace('>%i<'%today.day, 'bgcolor="#66ff66"><b>%i</b><'%today.day)

    # iterate through all LoginDate objects of the user
    date_objects = the_user.login_dates.all()
    # get the login_date from each
    dates = []
    for date_object in date_objects:
        dates.append(date_object.login_date)
    
    # get day number from each
    days = []
    for date in dates:
        days.append(date.day)

    # change colour if in days list
    for day in days:
        if day != today.day:
            cal = cal.replace('>%i<'%day, 'bgcolor="#39CCCC">%i<'%day)
    
    return cal

@login_required
def goal_tick(request, user_pk, goal_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    goal = get_object_or_404(Goal, user = the_user, pk = goal_pk)
    goal.completed = True
    goal.save()
    return redirect(f'/dashboard/{user_pk}/')

@login_required
def goal_edit(request, user_pk, goal_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    goal = get_object_or_404(Goal, user = the_user, pk = goal_pk)
    if (goal.editing == False):
        goal.editing = True
        goal.save()
        goals = Goal.objects.filter(completed=False, user = the_user)
        cal = colour_calendar(user_pk)
        return render(request, 'dashboard/base_dashboard_edit.html',{'goals':goals, 'cal':cal})
    else:
        goal.editing = False
        goal.text = request.POST.get('goal_cell_edit', goal.text)
        if (request.POST.get('date_cell_edit', '') != ''):
            goal.due_date = request.POST.get('date_cell_edit', goal.due_date)
        goal.save()
        return redirect(f'/dashboard/{user_pk}/')