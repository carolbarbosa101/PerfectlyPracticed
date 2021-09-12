from django.shortcuts import get_object_or_404, redirect, render
from users.models import MyUser
from .models import Song, Recording
from datetime import datetime
import os
import json
import boto3
from botocore.client import Config
from django.http import HttpResponse, HttpResponseForbidden
import urllib.parse as urlparse
import requests
from django.contrib import messages


def song_book(request, user_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden()
    songs = Song.objects.filter(user = the_user)
    to_learn_songs = songs.filter(status='to_learn').order_by('list_index')
    learning_songs = songs.filter(status='learning').order_by('list_index')
    learned_songs = songs.filter(status='learned').order_by('list_index')
    rusty_songs = songs.filter(status='rusty').order_by('list_index')
    recordings = Recording.objects.all().order_by('-dt')
    
    return render(request, 'song_book/base_songbook.html',{'to_learn_songs': to_learn_songs, 'learning_songs':learning_songs,
    'learned_songs': learned_songs, 'rusty_songs':rusty_songs, 'recordings':recordings, 'user':the_user})

def index_init(song):
    song.list_index = (song.pk - 1)
    song.save()

def song_post(request, user_pk, status):
    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden()
    
    if status == 'to_learn':
        song = Song.objects.create(text=request.POST['to_learn_input'], status = status, user = the_user)
        index_init(song)
        return redirect(f'/song_book/{user_pk}/')
    elif status == 'learning':
        song = Song.objects.create(text=request.POST['learning_input'] , status = status, user = the_user)
        index_init(song)
        return redirect(f'/song_book/{user_pk}/')
    elif status == 'learned':
        song = Song.objects.create(text=request.POST['learned_input'] , status = status, user = the_user)
        index_init(song)
        return redirect(f'/song_book/{user_pk}/')
    elif status == 'rusty':
        song = Song.objects.create(text=request.POST['rusty_input'] , status = status, user = the_user)
        index_init(song)
        return redirect(f'/song_book/{user_pk}/')

def song_delete(request, user_pk, song_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden()
    song = Song.objects.get(pk = song_pk, user=the_user)
    song.delete()
    return redirect(f'/song_book/{user_pk}/')

def song_move(request):
    user_pk = request.POST.get('user_pk')
    song_pk = request.POST.get('song_pk')
    list_index = request.POST.get('list_index')
    status = request.POST.get('status')
    
    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden()
    song = Song.objects.get(pk = song_pk, user=the_user)
    song.list_index = list_index
    song.status = status
    song.save()
    return redirect(f'/song_book/{user_pk}/')

def song_note(request):
    user_pk = request.POST.get('user_pk')
    song_pk = request.POST.get('song_pk')

    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden()
    song = Song.objects.get(pk = song_pk, user=the_user)
    song.note = request.POST.get('note_input')
    song.save()
    return redirect(f'/song_book/{user_pk}/')

def song_video(request, user_pk, song_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden()
    song = Song.objects.get(pk = song_pk, user=the_user)

    # method of validating link taken form here: 
    # https://stackoverflow.com/questions/63325908/how-do-i-check-if-a-youtube-video-url-is-valid-or-not-in-python
    # check if input is valid YouTube URL
    raw_link = request.POST['link_input']
    if raw_link.startswith('https://'):
        r = requests.get(raw_link)
        if "Video unavailable" in r.text:
            messages.warning(request, 'Please add a valid YouTube URL.')
            return redirect(f'/song_book/{user_pk}/')
    else:
        messages.warning(request, 'Please add a valid YouTube URL.')
        return redirect(f'/song_book/{user_pk}/')

    # url parse implementation taken from here: 
    # https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
    # turn regular yt link to embed link
    url_data = urlparse.urlparse(raw_link)
    query = urlparse.parse_qs(url_data.query)
    id = query["v"][0]
    embed_link = f'https://www.youtube.com/embed/{id}'
    song.video = embed_link
    song.save()
    return redirect(f'/song_book/{user_pk}/')

# following function adapted from these two source: 
# https://devcenter.heroku.com/articles/s3-upload-python
# https://github.com/boto/boto3/issues/934
def sign_s3(request, file_name):
    # this function signs off the wav file we want to send to AWS,
    # with the AWS details stored in environment variables 
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

    file_name = f'song_book/recordings/{file_name}'
    file_type = 'audio/wav'

    s3 = boto3.client('s3',
                      region_name='eu-west-2',
                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                      config=Config(signature_version='s3v4'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
                      )

    presigned_post = s3.generate_presigned_post(
        Bucket = AWS_STORAGE_BUCKET_NAME,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
            {'acl': "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    json_dump = json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.eu-west-2.amazonaws.com/%s' % (AWS_STORAGE_BUCKET_NAME, file_name),
    })

    return HttpResponse(json_dump, content_type='json')

def song_recording(request, user_pk, song_pk):
    f = request.POST.get('url')
    display_name = request.POST.get('display_name')

    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden()
    the_song = Song.objects.get(pk = song_pk, user=the_user)
    recording = Recording.objects.create(file=f, name=display_name, song=the_song)
    recording.save()

    return redirect(f'/song_book/{user_pk}/')


def song_recording_delete(request, user_pk, song_pk, recording_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden()
    the_song = Song.objects.get(pk = song_pk, user=the_user)
    recording = Recording.objects.get(pk=recording_pk, song=the_song)
    recording.delete()
    return redirect(f'/song_book/{user_pk}/')

