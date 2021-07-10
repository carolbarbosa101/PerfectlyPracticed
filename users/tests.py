from django.http import response
from django.test import TestCase
from django.urls import resolve

from users.models import MyUser

# Create your tests here.
class RegisterLoginTest(TestCase):

    def test_uses_login_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'users/login.html')

    def test_uses_sign_up_template(self):
        response = self.client.get('/sign_up')
        self.assertTemplateUsed(response, 'users/sign_up.html')
    
    def sign_up_POST(self):
        response = self.client.post('/sign_up', data={'email': 
        'user2@test.com', 'first_name':'User', 'last_name':'Test',
        'password1':'PassTest123', 'password2':'PassTest123'})
        return response

    def test_details_saved_after_POST(self):
        self.sign_up_POST()
        self.assertEqual(MyUser.objects.count(), 1)
        new_item = MyUser.objects.first()
        self.assertEqual(new_item.email, 'user2@test.com')
        self.assertEqual(new_item.first_name, 'User')
        self.assertEqual(new_item.last_name, 'Test')
        self.assertTrue(new_item.check_password('PassTest123'))

    def test_redirect_to_login_after_signup(self):
        response = self.sign_up_POST()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_successful_login(self):
        self.sign_up_POST()
        response = self.client.post('/', data={'username': 
        'user2@test.com','password':'PassTest123'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/success')
        
