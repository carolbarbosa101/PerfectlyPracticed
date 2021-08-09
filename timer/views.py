from django.shortcuts import render, redirect, get_object_or_404
from users.models import MyUser
from .models import Task
import json
from django.core.serializers.json import DjangoJSONEncoder

def timer(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    if request.method == 'POST':
        Task.objects.create(text=request.POST['task_input'] , time=request.POST['time_input'], colour=request.POST['colour_input'], user = the_user)
        return redirect(f'/timer/{pk}/')
    
    time_list = []
    colour_list = []
    tasks = Task.objects.filter(user = the_user)
    for task in tasks:
        time_list.append(task.time)
        colour_list.append(task.colour)

    time_list_json = json.dumps(list(time_list), cls=DjangoJSONEncoder)
    colour_list_json = json.dumps(list(colour_list), cls=DjangoJSONEncoder)
    
    return render(request, 'timer/base_timer.html', {'user':the_user, 'tasks':tasks, 'time_list': time_list_json, 'colour_list': colour_list_json})

def task_delete(request, user_pk, task_pk):
    the_user = get_object_or_404(MyUser, pk = user_pk)
    task = Task.objects.get(pk = task_pk, user=the_user)
    task.delete()
    return redirect(f'/timer/{user_pk}/')