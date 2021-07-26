from django.test import TestCase
from users.models import MyUser
from users.tests import RegisterLoginTest as rl

class TimerTest(TestCase):

    def test_timer_template_used(self):
        rl.sign_up_and_login(self)
        response = self.client.get('/timer/1/')
        self.assertTemplateUsed(response, 'timer/base_timer.html')

