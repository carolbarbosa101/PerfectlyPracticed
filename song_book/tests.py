from django.test import TestCase
from users.tests import RegisterLoginTest as rl

    
class SongBookTest(TestCase):   

    def test_song_book_template_used(self):
        rl.sign_up_and_login(self)
        response = self.client.get('/song_book/1/')
        self.assertTemplateUsed(response, 'song_book/base_songbook.html')
