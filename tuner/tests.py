from django.test import TestCase
from users.models import MyUser
from users.tests import RegisterLoginTest as rl

class TunerTest(TestCase):

    def test_tuner_template_used(self):
        rl.sign_up_and_login(self)
        response = self.client.get('/tuner/1/')
        self.assertTemplateUsed(response, 'tuner/base_tuner.html')
