from .base import FunctionalTest
import time
from selenium.webdriver.support.color import Color


class TimerTest(FunctionalTest):

    def test_timer(self):
        self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

        # Ziggy now wants to use the timer feature
        # He clicks on the link to it on dashboard
        self.find_and_click('.timer')

        # This takes him to the timer page
        self.assertIn('Timer', self.browser.title)
        
        # On the timer page he sees a circular countdown timer and a set of input boxes
        self.browser.find_element_by_css_selector('#timer_section')
        self.browser.find_element_by_css_selector('#input_section')

        # He types into the left input, the name of what a he wants to practice
        # And into the right input he sets the duration of time he wants to practice this
        self.find_and_fill_2('task_input', 'time_input', 'Starman chords', '15')
        self.find_and_fill_1('colour_input', 'rgb(255,0,0)')
        time.sleep(2)
        self.find_and_click('#add_button')

        # Upon adding this, he sees that the task and time have been listed below the input box 
        task_item_0 = self.browser.find_element_by_css_selector('#task_item_0')
        colour_item_0 = Color.from_string(task_item_0.value_of_css_property('background-color')).hex
        self.assertIn('Starman chords : 15 mins', task_item_0.text)


        # He also sees the time remaining display inside the timer changed to reflect the input
        time_remaining = self.browser.find_element_by_css_selector('#timer_label')
        self.assertEqual(time_remaining.text , '15:00')

        # He then clicks the start button and the countdown begins
        self.find_and_click('#timer_button')
        self.assertEqual(time_remaining.text , '15:00')

        # After 2 seconds he clicks the stop button and the countdown pauses
        time.sleep(2)
        self.find_and_click('#timer_button')
        self.assertEqual(time_remaining.text , '14:58')

        # H refreshes the page and sees the time reset / after adding a new task the page refreshes

        # He add another task to the timer now 
        self.find_and_fill_2('task_input', 'time_input', 'G Major Scale Improv', '10')
        self.find_and_fill_1('colour_input', 'rgb(0,255,0)')
        time.sleep(2)
        self.find_and_click('#add_button')
        task_item_1 = self.browser.find_element_by_css_selector('#task_item_1')
        colour_item_1 = Color.from_string(task_item_1.value_of_css_property('background-color')).hex


        # He now sees that the timer itself has its circle segmented into rings corresponding to each task
        # With the size of the ring being proportional to the time allocated to the task
        group = self.browser.find_elements_by_css_selector('.timer_circle')
        self.assertEqual(len(group), 3)

        # The colour of the task item listed also matches the colour of these segments
        self.assertIn('#ff0000', colour_item_0)
        self.assertIn('#00ff00', colour_item_1)

        # Once he hits start again he notices sees that the ring decreases in circumference as time elapses

        # Ziggy then decides he wants to practice something else so he adds another input

        # The timer changes again to have two different colours split into the fraction of time
        # each tasks is designated

        # And the time in the middle is set to be the total of the 2 tasks 

        # Ziggy adds a final task which is again changes the timer in a similar fashion 






