
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .list_page import ListPage
from .server_tools import create_session_on_server
User = get_user_model()


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # edith is a logged-in user
        self.create_pre_authenticated_session(email)
        
        # she goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item('Reticulate splines')
        list_page.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # she notices a "My lists" link, for the first time
        self.browser.find_element_by_link_text('My Lists').click()

        # she sees that her list is in there, names according to its first item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # she decides to start another list, just to see
        self.browser.get(self.live_server_url)
        list_page.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # under "my lists", her new list appears
        self.browser.find_element_by_link_text('My Lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # she logs out.  The "My Lists" option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My Lists'), []
        ))