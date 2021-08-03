from django.shortcuts import render, redirect
from users.models import MyUser
from .models import Timer, Task

def timer(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    if Timer.objects.filter(user = the_user).count() == 0:
        Timer.objects.create(total_time = 0, user = the_user)
    the_timer = Timer.objects.get(user=the_user)

    if request.method == 'POST':
        Task.objects.create(text=request.POST['task_input'] , time=request.POST['time_input'], timer = the_timer)
        the_timer = Timer.objects.get(user=the_user)
        the_timer.total_time += int(request.POST['time_input'])
        the_timer.save()
        return redirect(f'/timer/{pk}/')
    
    task_items = []
    tasks = Task.objects.filter(timer = the_timer)
    for task in tasks:
        task_item = f'{task.text} : {task.time} mins'
        if task_item not in task_items:
            task_items.append(task_item)
    

    return render(request, 'timer/base_timer.html', {'user':the_user, 'task_items':task_items, 'total_time':the_timer.total_time})
