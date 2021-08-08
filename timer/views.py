from django.shortcuts import render, redirect
from users.models import MyUser
from .models import Timer, Task
import json
from django.core.serializers.json import DjangoJSONEncoder

def timer(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    if Timer.objects.filter(user = the_user).count() == 0:
        Timer.objects.create(total_time = 0, user = the_user)
    the_timer = Timer.objects.get(user=the_user)

    if request.method == 'POST':
        Task.objects.create(text=request.POST['task_input'] , time=request.POST['time_input'], colour=request.POST['colour_input'], timer = the_timer)
        the_timer = Timer.objects.get(user=the_user)
        the_timer.total_time += int(request.POST['time_input'])
        the_timer.save()
        return redirect(f'/timer/{pk}/')
    
    time_list = []
    colour_list = []
    tasks = Task.objects.filter(timer = the_timer)
    for task in tasks:
        time_list.append(task.time)
        colour_list.append(task.colour)


    time_list_json = json.dumps(list(time_list), cls=DjangoJSONEncoder)
    colour_list_json = json.dumps(list(colour_list), cls=DjangoJSONEncoder)
    

    return render(request, 'timer/base_timer.html', {'user':the_user, 'total_time':the_timer.total_time, 
                'tasks':tasks, 'time_list': time_list_json, 'colour_list': colour_list_json})
