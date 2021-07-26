from .base import FunctionalTest
from datetime import datetime, timedelta
from users.models import LoginDate, MyUser
from PIL import ImageColor
    
class DashboardTest(FunctionalTest):
    
    def check_in_goals_table(self, col_id_1, col_id_2, row_content_1, row_content_2):
        rows = self.browser.find_elements_by_id(col_id_1)
        self.assertIn(row_content_1, [row.text for row in rows])
        rows = self.browser.find_elements_by_id(col_id_2)
        self.assertIn(row_content_2, [row.text for row in rows])

    def check_not_in_goals_table(self, col_id_1, col_id_2, row_content_1, row_content_2):
        rows = self.browser.find_elements_by_id(col_id_1)
        self.assertNotIn(row_content_1, [row.text for row in rows])
        rows = self.browser.find_elements_by_id(col_id_2)
        self.assertNotIn(row_content_2, [row.text for row in rows])
    

    def test_dashboard(self):  
        self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')
        
        # He can see there is button links to each of the features of the app
        self.browser.find_element_by_css_selector('.timer')
        self.browser.find_element_by_css_selector('.song_book')
        self.browser.find_element_by_css_selector('.metronome ')
        self.browser.find_element_by_css_selector('.tuner')
        self.browser.find_element_by_css_selector('.log')

        # He can see links to the profile, settings and log out cal
        self.browser.find_element_by_css_selector('.profile')
        self.browser.find_element_by_css_selector('.settings_link')
        self.browser.find_element_by_css_selector('.logout')

        # He clicks the logout button and it redirects him back to the login page
        self.find_and_click('.logout')
        self.assertIn('Music Practice', self.browser.title)  

        # When he tries to access the dashbaord again with a url, the website prompt for him to login again
        self.browser.get(self.live_server_url + '/dashboard/1/')
        self.assertIn('Music Practice', self.browser.title)  


    def test_dashboard_goals(self): 
        self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

        # He sees a section where he can set goals

        # He starts by adding a goal with a due date
        self.find_and_fill_2('goal_input', 'date_input', 'Learn the song Starman', '2021-08-01')
        self.find_and_click('#add_button')

        # He sees that this goal and due date now appears on the page
        self.check_in_goals_table('goal_cell', 'date_cell', 'Learn the song Starman', 'Aug. 1, 2021')

        # He then tries editing this goal to have different goal text and due date
        self.find_and_click('.edit_button')
        self.find_and_fill_2('goal_cell_edit', 'date_cell_edit', 'Learn the song Heroes', '2021-08-31')
        self.find_and_click('#save_button')

        # He sees that the goal and date have been sucessfully updated
        self.check_in_goals_table('goal_cell', 'date_cell', 'Learn the song Heroes', 'Aug. 31, 2021')

        # He adds another goal 
        self.find_and_fill_2('goal_input', 'date_input', 'Master G Major Scale 1st Position', '2021-09-15')
        self.find_and_click('#add_button')

        # And sees this goal also appears sucessfully, along with the previously added goal
        self.check_in_goals_table('goal_cell', 'date_cell', 'Master G Major Scale 1st Position', 'Sept. 15, 2021')
        self.check_in_goals_table('goal_cell', 'date_cell', 'Learn the song Heroes', 'Aug. 31, 2021')

        # He ticks off that he completed this goal 
        self.find_and_click('#checkbox')

        # And he sees the goal now dissappears from the page
        self.check_not_in_goals_table('goal_cell', 'date_cell', 'Learn the song Heroes', 'Aug. 31, 2021')

        # He tries adding another goal, this time omitting the due date
        self.find_and_fill_1('goal_input', 'Learn the F barre chord')
        self.find_and_click('#add_button')

        # He sees that the date section now shows as 'None'
        self.check_in_goals_table('goal_cell', 'date_cell', 'Learn the F barre chord', 'None')
       
        # He then edits this goal to now set a due date 
        self.find_and_click('.edit_button')
        self.find_and_fill_2('goal_cell_edit', 'date_cell_edit', 'Learn the F barre chord', '2021-12-31')
        self.find_and_click('#save_button')
        
        # And sees this change sucessfully happens
        self.check_in_goals_table('goal_cell', 'date_cell', 'Learn the F barre chord', 'Dec. 31, 2021')

        # Ziggy tries to click add with an empty goal text input
        self.find_and_fill_1('goal_input', '')
        self.find_and_click('#add_button')

        # This fails and an alert pops up saying 'Please enter a goal.'
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertIn('Please enter a goal.', alert.text)
        # self.fail('Finish the test!')  

    def add_login_date_and_check_colour(self, delta, colour):
        today = datetime.today()
        date_to_add = today - timedelta(days=delta)
        the_user = MyUser.objects.get(email='user1@test.com')
        LoginDate.objects.create(user=the_user, login_date=date_to_add)
        self.browser.refresh()
        cal = self.browser.find_element_by_id('calendar')
        elements = cal.find_elements_by_tag_name('td')
        for element in elements:
            if (element.text == str(date_to_add.day)):
                date_tag = element
                break
            else:
                date_tag = None
        self.assertEqual(str(date_to_add.day), date_tag.text)
        rgb_color = ImageColor.getcolor(colour, 'RGB')
        self.assertEqual(date_tag.value_of_css_property('background-color'), f'rgb{rgb_color}')

    def test_dashboard_calendar(self): 
        self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

        # He also sees a calendar to the right

        # He sees that the current day is highlighted and in bold on the calendar
        self.add_login_date_and_check_colour(0, '#66ff66')

        # (for the purposes of the test today's date will not be changed and login dates are added for previous days )
        # Ziggy logs in the next day and sees yesterday's date has a non-white colour (different to the colour of today's date),
        # to highlight that he logged in yesterday
        self.add_login_date_and_check_colour(4, '#39CCCC')

        # Ziggy then misses a day and when logs in the following day he sees that 
        # yesterday's date stays white, showing he didn't log in 
        today = datetime.today()
        date_to_add = today + timedelta(days=3)
        self.browser.refresh()
        cal = self.browser.find_element_by_id('calendar')
        elements = cal.find_elements_by_tag_name('td')
        for element in elements:
            if (element.text == str(date_to_add.day)):
                date_tag = element
                break
            else:
                date_tag = None
        self.assertEqual(str(date_to_add.day), date_tag.text)
        self.assertEqual(date_tag.value_of_css_property('background-color'), 'rgba(0, 0, 0, 0)')

        # But today's date still changes colour
        self.add_login_date_and_check_colour(2, '#39CCCC')
        
        # When he logs in the following day, he sees the past two days have changed colour
        self.add_login_date_and_check_colour(1, '#39CCCC')