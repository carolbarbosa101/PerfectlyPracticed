from .base import FunctionalTest
import time


class TunerTest(FunctionalTest):

    def test_tuner(self):
        self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

        # Ziggy now needs to tuner his guitar
        # He clicks on the link to it on dashboard
        self.find_and_click('.tuner')

        # This takes him to the tuner page
        self.assertIn('Tuner', self.browser.title)

        # He sees a button to start the tuner and clicks it
        self.find_and_click('#start_button')

        # Ziggy starts plucking the strings on his guitar and he sees feedback saying which note he is at

        # He also sees some frequency references below 
        # Deciding he wants to tune his bass as well, he clicks on the appropriate tab to see the info
        self.find_and_click('#v-pills-bass-tab')
        bass_ref = self.browser.find_element_by_css_selector('.tab-pane.show.active')
        self.assertIn('-- 4th String - E1 - 41.20Hz --', bass_ref.text)

