from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    def test_register_and_login(self):  
        # Ziggy has heard about this cool new website to help with his guitar practice
        # He opens his browser and goes to link
        self.browser.get(self.live_server_url)

        # He is presented with a login page with username and password textboxes
        self.assertIn('Music Hub', self.browser.title)  

        # Ziggy does not have an account so he chooses the sign up link that is below the entry fields
        time.sleep(2)
        sign_up_link = self.browser.find_element_by_link_text("Sign Up")
        sign_up_link.click()
        
        # He enters his details into the boxes and clicks the register button
        fname_input = self.browser.find_element_by_id('fname')
        fname_input.send_keys('Anwin')

        lname_input = self.browser.find_element_by_id('lname')
        lname_input.send_keys('Robin')

        email_input = self.browser.find_element_by_id('email')
        email_input.send_keys('user@test.com')

        pass_input = self.browser.find_element_by_id('password')
        pass_input.send_keys('pass1')

        time.sleep(2)
        sign_up_button = self.browser.find_element_by_id('sign_up_button')
        sign_up_button.click()
        time.sleep(2)

        # He is redirected to the login page again now 
        # Ziggy enters his details and sucessfully logs in
        email_input = self.browser.find_element_by_id('email')
        email_input.send_keys('user@test.com')

        pass_input = self.browser.find_element_by_id('password')
        pass_input.send_keys('pass1')

        login_button = self.browser.find_element_by_id('login_button')
        login_button.click()

        # He is now re-directed to his dashboard

        self.fail('Finish the test!')  





    