from .base import FunctionalTest
import time


class TunerTest(FunctionalTest):

    def test_tuner(self):
        self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

        # Ziggy now wants to use the timer feature
        # He clicks on the link to it on dashboard
        self.find_and_click('.tuner')

        # This takes him to the timer page
        self.assertIn('Tuner', self.browser.title)

        # He sees a button to start the tuner and clicks it
        self.find_and_click('#start_button')

        # Ziggy starts plucking the strings on his guitar and he sees feedback saying which note he is at
