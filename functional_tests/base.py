from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, HASH_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from users.models import MyUser
from selenium.webdriver.firefox.options import Options

# The first chapter of this book has been used extensively to make all the tests:
# https://www.obeythetestinggoat.com/book/part1.harry.html



# parent class with helper methods for other functional tests
class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):  
        # following line from here: 
        # https://stackoverflow.com/questions/21310797/using-selenium-webdriver-and-python-how-do-i-suppress-the-prompt-to-share-my-ca
        options = Options()
        options.set_preference("media.navigator.permission.disabled", True)
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):  
        self.browser.quit()
    
    def create_pre_authenticated_session(self, email, password, first_name, last_name):
        user = MyUser.objects.create(email=email, password=password, first_name=first_name, last_name=last_name)
        session = SessionStore()
        session[SESSION_KEY] = user.pk 
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()
        ## to set a cookie we need to first visit the domain.
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key, 
            secure = False,
            path='/',
        ))
        self.browser.refresh()
        self.browser.get(f'{self.live_server_url}/dashboard/{user.pk}/')

    def find_and_fill_1(self, name, input):
        element = self.browser.find_element_by_name(name)
        element.clear()
        element.send_keys(input)

    def find_and_fill_2(self, name_1, name_2, input_1, input_2):
        element = self.browser.find_element_by_name(name_1)
        element.clear()
        element.send_keys(input_1)
        element = self.browser.find_element_by_name(name_2)
        element.clear()
        element.send_keys(input_2)
    
    def find_and_click(self, selector):
        button = self.browser.find_element_by_css_selector(selector)
        button.click()
