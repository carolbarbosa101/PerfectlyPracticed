from .base import FunctionalTest


class SongBookTest(FunctionalTest):

    def test_song_book(self):
        self.create_pre_authenticated_session('user1@test.com', 'PassTest123', 'User', 'Test')

        # Ziggy now wants to track the songs that he has been learning
        # He clicks on the link to the song book feature
        self.find_and_click('.song_book')

        # This takes him to the song book page
        self.assertIn('Song Book', self.browser.title)
        
        # On the page he sees a kanban board style layout where he can add songs to different sections

        # He chooses to add Starman to the 'learning' section

        # The element appears in this section now after adding 

        # When he clicks on Starman song element he is brought to its page
        
        # Here he can add text and images

        # Add a youtube link to tutorials

        # Record his practise attempts of the song  