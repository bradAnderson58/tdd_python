
import os
import poplib
import re
import time
from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['YAHOO_PASSWORD'])
            while time.time() - start < 60:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.delete(email_id)
            inbox.quit()

    def test_can_get_email_link_to_login_in(self):
        # edith goes to the awesome superlists site
        # and notices a log in section in the navbar for the first time
        # its telling her to enter her email address, so she does
        test_email = 'brad.a80@yahoo.com' if self.staging_server else 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # a message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email', self.browser.find_element_by_tag_name('body').text
        ))

        # she checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # it has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_to_be_logged_in(email=test_email)
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(test_email, navbar.text)

        # now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # she is logged out
        self.wait_to_be_logged_out(email=test_email)
