from django.shortcuts import get_object_or_404, redirect, render
from users.models import MyUser
from .models import Song

def song_book(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    songs = Song.objects.filter(user = the_user)
    return render(request, 'song_book/base_songbook.html',{'songs': songs, 'user':the_user})


def song_post(request, pk, status_num):
    the_user = MyUser.objects.get(pk=pk)
    
    if status_num == 1:
        Song.objects.create(text = request.POST.get('to_learn_input', 'A song'), status = 'to_learn', user = the_user)
        return redirect(f'/song_book/{pk}/')
    elif status_num == 2:
        Song.objects.create(text=request.POST['learning_input'] , status = 'learning', user = the_user)
        return redirect(f'/song_book/{pk}/')
    elif status_num == 3:
        Song.objects.create(text=request.POST['learned_input'] , status = 'learned', user = the_user)
        return redirect(f'/song_book/{pk}/')
    elif status_num == 4:
        Song.objects.create(text=request.POST['rusty_input'] , status = 'rusty', user = the_user)
        return redirect(f'/song_book/{pk}/')

def song_delete(request, user_pk, song_pk):
    the_user = get_object_or_404(MyUser, pk = user_pk)
    song = Song.objects.get(pk = song_pk, user=the_user)
    song.delete()
    return redirect(f'/song_book/{user_pk}/')
