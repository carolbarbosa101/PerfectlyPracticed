from django.shortcuts import render, redirect
from users.models import MyUser
from .models import Task

def timer(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    if request.method == 'POST':
        Task.objects.create(text=request.POST['task_input'] , time=request.POST['time_input'], user = the_user)
        redirect('/timer/1/')
    
    tasks = Task.objects.all()
    task_items = []
    for task in tasks:
        task_item = f'{task.text} : {task.time} mins'
        if task_item not in task_items:
            task_items.append(task_item)

    return render(request, 'timer/base_timer.html', {'user':the_user, 'task_items':task_items})
