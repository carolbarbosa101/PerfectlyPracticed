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


        # He add another task to the timer now 
        # After adding a new task the page refreshes resetting the timer 
        self.find_and_fill_2('task_input', 'time_input', 'G Major Scale Improv', '10')
        self.find_and_fill_1('colour_input', 'rgb(0,255,0)')
        self.find_and_click('#add_button')
        task_item_1 = self.browser.find_element_by_css_selector('#task_item_1')
        colour_item_1 = Color.from_string(task_item_1.value_of_css_property('background-color')).hex


        # He now sees that the timer itself has its circle segmented into rings corresponding to each task
        # With the size of the segments being proportional to the time allocated to the task
        # (offset of current task corresponds to fraction of previous task)

        circle_1 = self.browser.find_element_by_css_selector('#circle_1')
        offset_1 = float(circle_1.get_attribute('stroke-dashoffset'))
        predicted_fraction_0 = round(abs(offset_1) / 1885, 2)
        actual_fraction_0 = 15/25
        self.assertEqual(predicted_fraction_0, actual_fraction_0)

        # And the time in the centre corresponding to the total time of the two tasks
        time_remaining = self.browser.find_element_by_css_selector('#timer_label')
        self.assertEqual(time_remaining.text , '25:00')

        # The colour of the task item listed also matches the colour of these segments

        # Once he hits start again he notices sees that the ring decreases in circumference as time elapses
        self.find_and_click('#timer_button')
        circle_top_path = self.browser.find_element_by_css_selector('#circle_top_path')
        top_offset = float(circle_top_path.get_attribute("stroke-dashoffset"))
        # offset is full circumference at the start
        self.assertEqual(top_offset, -1885)
        time.sleep(3)
        # after 3 seconds the offset has decreased to decrease the timer circumference
        top_offset = round(float(circle_top_path.get_attribute("stroke-dashoffset")))
        self.assertAlmostEqual(top_offset, -1881)

        # Ziggy then decides to remove one of the tasks, so clicks the delete button on the task item
        # He sees the timer update to reflect the deletion
        self.find_and_click('#delete_button_1')
        time_remaining = self.browser.find_element_by_css_selector('#timer_label')
        self.assertEqual(time_remaining.text , '15:00') 







