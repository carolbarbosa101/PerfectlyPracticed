from .base import FunctionalTest
    
class SignupLoginTest(FunctionalTest):
    
    def test_register_and_login(self):  
        # Ziggy has heard about this cool new website, 
        # that can help his guitar practice
        # He opens his browser and goes to the link
        self.browser.get(self.live_server_url)

        # He is presented with a login page with username and password textboxes
        self.assertIn('Perfectly Practiced', self.browser.title)  

        # Ziggy does not have an account,
        # so he chooses the sign up link that is below the entry fields
        self.find_and_click('#sign_up')
        
        # He enters his details into the boxes and clicks the register button
        self.find_and_fill_1('email', 'user1@test.com')
        self.find_and_fill_1('first_name', 'User')
        self.find_and_fill_1('last_name', 'Test')
        self.find_and_fill_1('password1', 'PassTest123')
        self.find_and_fill_1('password2', 'PassTest123')
        self.find_and_click(".btn")

        # He is redirected to the login page again now 
        # Ziggy enters his details and sucessfully logs in
        self.find_and_fill_2('username', 'password', 'user1@test.com', 'PassTest123')
        self.find_and_click(".btn")

        # He is now re-directed to his dashboard
        self.assertIn('dashboard', self.browser.current_url)