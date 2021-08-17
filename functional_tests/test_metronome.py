from .base import FunctionalTest
import time
from selenium.webdriver.common.keys import Keys


class MetronomeTest(FunctionalTest):

    def animationOpacity(self):
            animated_circle = self.browser.find_element_by_css_selector('#circle_2')
            opacity = round(float(animated_circle.value_of_css_property('opacity')), 1)
            return opacity

    def test_metronome(self):
            self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

            # Ziggy now wants to use the timer feature
            # He clicks on the link to it on dashboard
            self.find_and_click('.metronome')

            # This takes him to the timer page
            self.assertIn('Metronome', self.browser.title)

            # He sees a simple layout with a circle, the current bpm and a slider range input to adjust the bpm

            # He starts off by playing the metronome at the default 60bpm
            self.find_and_click('#play_button')

            # He hears a clicking sound in the 60 bpm tempo provided

            # He sees a flashing animation on the circle as well, in time with the clicking sound
            # (animation reduces opacity to 0.5 within 0.2s for a tempo of < 120 bpm)
            time.sleep(0.2)
            opacity = self.animationOpacity()
            self.assertEqual(opacity, 0.5)

            # When he slides the slider across to 130 bpm he notices the tempo of the sound and animation increase
            # (unfortunately the sound and animation becomes very off-sync in this test )
            slider = self.browser.find_element_by_css_selector('#bpm_input')
            for i in range(70):
                slider.send_keys(Keys.RIGHT)
            # (animation reduces opacity to 0.5 within 0.1s for a tempo > 120 bpm)
            time.sleep(0.1)
            opacity = self.animationOpacity()
            self.assertEqual(opacity, 0.5)
            
            # Finally when clicks the pause button the sound and animation stops
            self.find_and_click('#pause_button')
            opacity = self.animationOpacity()
            self.assertEqual(opacity, 0.5)
            # (no further change in animation)
            time.sleep(0.1)
            self.assertEqual(opacity, 0.5)
