from django.test import TestCase

# Create your tests here.
class LoginPageTest(TestCase):

    def test_uses_login_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'musicapp/login_page.html')

    def test_sign_up_link(self):
        pass

    def test_uses_sign_up_template(self):
        pass

    def test_redirect_to_login(self):
        pass

    def test_redirect_to_dashboard(self):
        pass