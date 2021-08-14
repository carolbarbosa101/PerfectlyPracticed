from .base import FunctionalTest
from selenium.webdriver.common.action_chains import ActionChains 
import time
from selenium import webdriver


class SongBookTest(FunctionalTest):

    def test_song_book(self):
        self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

        # Ziggy now wants to track the songs that he has been learning
        # He clicks on the link to the song book feature
        self.find_and_click('.song_book')

        # This takes him to the song book page
        self.assertIn('Song Book', self.browser.title)
        
        # On the page he sees a kanban board style layout where he can add songs to different sections
        self.browser.find_element_by_css_selector('#board')

        # He chooses to add Starman to the 'learning' section
        self.find_and_fill_1('learning_input', 'Starman')
        self.find_and_click('#learning_submit')

        # The element appears in this section now after adding 
        song = self.browser.find_element_by_css_selector('#song_5_1') # user_pk = 5 due to 5th login with all tests
        self.assertIn('Starman', song.text)

        # He adds in a few more songs into different sections
        self.find_and_fill_1('to_learn_input', 'Heroes')
        self.find_and_click('#to_learn_submit')
        self.find_and_fill_1('learning_input', 'Life On Mars')
        self.find_and_click('#learning_submit')
        self.find_and_fill_1('learned_input', 'Space Oddity')
        self.find_and_click('#learned_submit')
        self.find_and_fill_1('rusty_input', 'Under Pressure')
        self.find_and_click('#rusty_submit')
        self.find_and_fill_1('rusty_input', 'Lets Dance')
        self.find_and_click('#rusty_submit')

        # He then deletes one of the songs 
        list_group = self.browser.find_element_by_css_selector('#rusty_list')
        list_group_children = list_group.find_elements_by_tag_name('li')
        self.assertEqual(len(list_group_children), 2)
        self.find_and_click('#rusty_delete')
        list_group = self.browser.find_element_by_css_selector('#rusty_list')
        list_group_children = list_group.find_elements_by_tag_name('li')
        self.assertEqual(len(list_group_children), 1)

        # Rearranging items is also possible (see song_book/tests.py, not possible in selenium for sortable js)
        
        # When he clicks on Starman song element he is brought to its page
        
        # Here he can add text and images

        # Add a youtube link to tutorials

        # Record his practice attempts of the song  

