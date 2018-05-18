from .base import FunctionalTest
from .list_page import ListPage
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        list_page = ListPage(self)

        # she notices the input box is nicely centered
        inputbox = list_page.get_item_input_box()
        position = inputbox.location['x'] + inputbox.size['width'] / 2
        self.assertAlmostEqual(position, 512, delta=10)

        # she starts a new list and sees the input is nicely centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('testing', 1)
        inputbox = list_page.get_item_input_box()
        position = inputbox.location['x'] + inputbox.size['width'] / 2
        self.assertAlmostEqual(position, 512, delta=10)
