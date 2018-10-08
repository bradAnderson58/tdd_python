from .base import FunctionalTest
from .list_page import ListPage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_list_for_one_user(self):
        # User has heard about cool new online to-do app
        # goes to check out the homepage
        self.browser.get(self.live_server_url)

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to ented a to-do item straight away
        list_page = ListPage(self)
        inputbox = list_page.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # User types "Buy peacock feathers" into text box
        inputbox.send_keys('Buy peacock feathers')

        # When user hits enter, the page updates, and now the page lists:
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Buy peacock feathers', 1)

        # There is still a text box inviting the user to add another item
        # User enters "Use peacock feathers to make fly"
        inputbox = list_page.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, now both items are listed
        list_page.wait_for_row_in_list_table('Buy peacock feathers', 1)
        list_page.wait_for_row_in_list_table('Use peacock feathers to make fly', 2)


    def test_multiple_users_can_start_lists_with_different_urls(self):
        # User1 (Edith) starts a new todo list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item('Buy peacock feathers')

        # User notices that her list has a unique url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # New user (Francis) visits the site
        ## we use a new browser session to make sure that no edith info comes through
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the homepage, does not see Ediths list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make fly', page_text)

        # Francis starts a new list
        list_page.add_list_item('Buy milk')

        # Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # there is still no edith items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
