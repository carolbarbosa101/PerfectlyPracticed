from selenium import webdriver
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):  
        self.browser = webdriver.Firefox()

    def tearDown(self):  
        self.browser.quit()

    # Ziggy has heard about this cool new website to help with his guitar practice
    # He opens his browser and goes to link
    def test_open_site_and_check_title(self):  
        self.browser.get('http://localhost:8000')
        self.assertIn('Music Hub', self.browser.title)  
        
        self.fail('Finish the test!')  

    # He is presented with a login page with username and password textboxes
    # Ziggy does not have an account so he chooses the sign up option that is below the entry fields

    # He enters his details into the boxes and clicks the register button
    def test_registration(self):
        pass

    # He is redirected to the login page again now 
    # Ziggy enters his details and sucessfully logs in
    def test_login(self):
        pass

    # He is now re-directed to his dashboard


    