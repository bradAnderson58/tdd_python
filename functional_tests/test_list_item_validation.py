from .base import FunctionalTest
from .list_page import ListPage
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # edith goes to the home page and accidentally tries to submit an empty item
        # she hits enter on the empty input box
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # the browser intercepts the request, and does NOT load list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # she tries again with some text for the item, and the error disappears
        list_page.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))

        # and she can submit it successfully
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Buy milk', 1)

        # perversely, she now decides to submit a second blank list item
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # again the browser will not comply
        list_page.wait_for_row_in_list_table('Buy milk', 1)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # and she can correct it by filling in some text
        list_page.add_list_item('Make tea')
        list_page.wait_for_row_in_list_table('Buy milk', 1)
        list_page.wait_for_row_in_list_table('Make tea', 2)

    def test_cannot_add_duplicate_items(self):
        # edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item('Buy wellies')

        # she accidentally tries to enter a duplicate item
        list_page.get_item_input_box().send_keys('Buy wellies')
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # she sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text, "The fields list, text must make a unique set.")
        )
        
    def test_error_messages_cleared_on_input(self):
        # edith starts with a list and causes a validation error
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item('Banter too thick')
        list_page.get_item_input_box().send_keys('Banter too thick')
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # she starts typing in the input box to clear the error
        list_page.get_item_input_box().send_keys('a')

        # she is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
