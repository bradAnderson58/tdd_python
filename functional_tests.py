from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User has heard about cool new online to-do app
        # goes to check out the homepage
        self.browser.get('http://localhost:8000')

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # User is invited to ented a to-do item straight away

        # User types "Buy peacock feathers" into text box

        # When user hits enter, the page updates, and now the page lists:
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting the user to add another item
        # User enters "Use peacock feathers to make fly"

        # The page updates again, now both items are listed

        # User notices site has generated a unique URL for their list
        # There is some explanatory text to that effect

        # User visits that URL - the to-do list is still there

if __name__ == '__main__':
    unittest.main()