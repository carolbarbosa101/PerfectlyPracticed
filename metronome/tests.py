from django.test import TestCase

from django.test import TestCase
from users.tests import RegisterLoginTest as rl
from .models import Metronome
from users.models import MyUser

    
class SongBookTest(TestCase):   

    def test_metronome_template_used(self):
        rl.sign_up_and_login(self)
        response = self.client.get('/metronome/1/')
        self.assertTemplateUsed(response, 'metronome/base_metronome.html')
