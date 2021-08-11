from django.test import TestCase
from users.tests import RegisterLoginTest as rl
from .models import Song
from users.models import MyUser

    
class SongBookTest(TestCase):   

    def test_song_book_template_used(self):
        rl.sign_up_and_login(self)
        response = self.client.get('/song_book/1/')
        self.assertTemplateUsed(response, 'song_book/base_songbook.html')
    
    def test_song_input_saved(self):
        rl.sign_up_and_login(self)
        self.client.post('/song_book/1/song_post/2/', data={'learning_input' : 'Starman'})
        new_item = Song.objects.first()
        self.assertEqual(new_item.text, 'Starman')
        self.assertEqual(new_item.status, 'learning')
    
    def test_song_delete(self):
        rl.sign_up_and_login(self)
        the_user = MyUser.objects.get(pk=1)
        self.client.post('/song_book/1/song_post/2/', data={'learning_input' : 'Starman'})
        self.client.post('/song_book/1/song_post/4/', data={'rusty_input' : 'Under Pressure'})
        songs = Song.objects.filter(user=the_user)
        self.assertEqual(songs.count(), 2)
        self.client.post('/song_book/1/song_delete/2/')
        self.assertEqual(songs.count(), 1)


