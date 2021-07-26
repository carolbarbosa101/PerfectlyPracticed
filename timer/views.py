from django.shortcuts import render
from users.models import MyUser

def timer(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    return render(request, 'timer/base_timer.html', {'user':the_user})
