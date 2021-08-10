from django.shortcuts import get_object_or_404, redirect, render
from users.models import MyUser

def song_book(request, pk):
    the_user = MyUser.objects.get(pk=pk)

    return render(request, 'song_book/base_songbook.html',{'user':the_user})
