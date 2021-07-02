from django.http import response
from django.test import TestCase
from django.urls import resolve

# Create your tests here.
class LoginPageTest(TestCase):

    def test_uses_login_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'musicapp/login_page.html')

    def test_uses_sign_up_template(self):
        response = self.client.get('/sign_up')
        self.assertTemplateUsed(response, 'musicapp/sign_up.html')

    def test_details_registered(self):
        pass

    def test_redirect_to_login(self):
        pass

    def test_login_details_match(self):
        pass

    def test_redirect_to_dashboard(self):
        pass