from .base import FunctionalTest

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
        self.find_and_fill_1('colour_pick', '#FF0000')
        self.find_and_click('#add_button')

        # Upon adding this, he sees that the task and time have been listed below the input box 
        task_item = self.browser.find_element_by_css_selector('#task_item')
        self.assertIn('Starman chords : 15 mins', task_item.text)

        # He also sees the time remaining display inside the timer changed to reflect the input
        time_remaining = self.browser.find_element_by_css_selector('#timer_label')
        self.assertEqual(time_remaining.text , '15:00')

        # The colour of the task item listed matches the line inside the timer as well
        # self.assertEqual(task_item.colour , '#FF0000')


        # He then clicks the start button and the countdown begins
        # self.find_and_click('timer_button')

        # He sees the coloured ring decrease in circumference as time elapses

        # Ziggy then decides he wants to practice something else so he adds another input

        # The timer changes again to have two different colours split into the fraction of time
        # each tasks is designated

        # And the time in the middle is set to be the total of the 2 tasks 

        # Ziggy adds a final task which is again changes the timer in a similar fashion 






