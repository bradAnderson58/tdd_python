from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # edith goes to the home page and accidentally tries to submit an empty item
        # she hits enter on the empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # the home page refreshes, and there is an error message saying
        # 'List items cannot be blank'
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text, "You can't have an empty list item")
        )

        # she tries again with some text for the item, which now works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # perversely, she now decides to submit a second blank list item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # she receives a similar warning on the list page
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text, "You can't have an empty list item")
        )

        # and she can correct it by filling in some text
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')