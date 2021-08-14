from .base import FunctionalTest
import time


class MetronomeTest(FunctionalTest):

    def test_metronome(self):
            self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

            # Ziggy now wants to use the timer feature
            # He clicks on the link to it on dashboard
            self.find_and_click('.metronome')

            # This takes him to the timer page
            self.assertIn('Metronome', self.browser.title)