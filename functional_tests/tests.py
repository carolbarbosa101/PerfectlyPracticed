from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time
import random

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def find_and_fill(self, name, input):
        element = self.browser.find_element_by_name(name)
        element.send_keys(input)

    def test_register_and_login(self):  
        # Ziggy has heard about this cool new website to help with his guitar practice
        # He opens his browser and goes to link
        self.browser.get(self.live_server_url)

        # He is presented with a login page with username and password textboxes
        self.assertIn('Music Practice', self.browser.title)  

        # Ziggy does not have an account so he chooses the sign up link that is below the entry fields
        sign_up_link = self.browser.find_element_by_link_text("Sign Up")
        sign_up_link.click()
        
        # He enters his details into the boxes and clicks the register button
        self.find_and_fill('email', 'user1@test.com')
        self.find_and_fill('first_name', 'User')
        self.find_and_fill('last_name', 'Test')
        self.find_and_fill('password1', 'PassTest123')
        self.find_and_fill('password2', 'PassTest123')

        sign_up_button = self.browser.find_element_by_tag_name('button')
        sign_up_button.click()

        # He is redirected to the login page again now 
        # Ziggy enters his details and sucessfully logs in
        self.find_and_fill('username', 'user1@test.com')
        self.find_and_fill('password', 'PassTest123')

        login_button = self.browser.find_element_by_tag_name('button')
        login_button.click()
        time.sleep(2)

        # He is now re-directed to his dashboard

        # self.fail('Finish the test!')  





    