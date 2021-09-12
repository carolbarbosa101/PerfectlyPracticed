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
        song = self.browser.find_element_by_css_selector('#song_6_1') # user_pk = 6 due to 6th login with all tests
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
        list_group_children = self.browser.find_elements_by_css_selector('#rusty_list > li')
        self.assertEqual(len(list_group_children), 2)
        self.find_and_click('#song_6_6 > a')
        list_group_children = self.browser.find_elements_by_css_selector('#rusty_list > li')
        self.assertEqual(len(list_group_children), 1)

        # Rearranging items is also possible (see song_book/tests.py, not possible in selenium for sortable js)
        
        # When he clicks on Heroes song element he is brought to its pop up box
        self.find_and_click('#song_6_2')
        self.browser.switch_to.active_element

        # Here he sees he can embed a youtube tutorial link by pasting in the URL
        self.find_and_fill_1('link_input', 'https://www.youtube.com/watch?v=aWOppc3Udto&ab_channel=LeftHandedGuitarist')
        self.find_and_click('.btn.btn-outline-success')

        # When he opens the pop up box again he sees the video he selected is now embeded
        self.find_and_click('#song_6_2')
        self.browser.switch_to.active_element
        iframe = self.browser.find_element_by_css_selector('.vid_frame')
        link = iframe.get_attribute('src')
        self.assertEqual(link, 'https://www.youtube.com/embed/aWOppc3Udto')
        
        # And beneath this he can write and save notes about the video
        self.find_and_click('.note_p')
        self.find_and_fill_1('note_input', 'Verse chords are D, Am, C and G')
        self.find_and_click('.btn.btn-success.float-right')
        note = self.browser.find_element_by_css_selector('.note_p')
        self.assertEqual(note.text, 'Verse chords are D, Am, C and G')

        # He now swtiches to the recordings tab
        self.find_and_click('#recordings-tab')

        # Here he can record practice attempts of the song
        self.find_and_click('.record_button')
        time.sleep(2)
        # He can pause in the middle of his recording
        self.find_and_click('.pause_button')
        # And when he is done, he hits stop 
        self.find_and_click('.stop_button')

        # He then sees a preview where he can listen back to the recording 
        # following line taken from here: 
        # https://stackoverflow.com/questions/53515607/how-to-handle-html-audio-element-in-selenium
        self.browser.execute_script("document.getElementsByClassName('preview-audio')[0].play()")
        time.sleep(2)

        # In the preview he sees options to save or discard the recording
        # Ziggy doesn't like his first recording, so he click discard and sees the recording removed
        self.find_and_click('.btn.btn-danger.discard')

        # Ziggy records another one and this time chooses to save this
        self.find_and_click('.record_button')
        time.sleep(2)
        self.find_and_click('.stop_button')
        self.find_and_click('.btn.btn-success.save')

        # He then sees prompt which asks him to name the recording
        # He gives it a name and hits ok
        alert = self.browser.switch_to.alert
        alert.send_keys('heroes_rec')
        alert.accept()
        time.sleep(2)

        # Upon re-opening the pop up, he sees his previous recording saved
        self.find_and_click('#song_6_2')
        self.browser.implicitly_wait(10)
        self.browser.switch_to.active_element
        self.find_and_click('#recordings-tab')
        recording = self.browser.find_element_by_tag_name('li')

