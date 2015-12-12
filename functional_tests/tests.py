import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        assert any(row.text == row_text for row in rows),\
            "A new todo item did not appear in the tables. Its text was:\n%s" % table.text

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        # She notices the page title and header mention to-do lists
        assert 'Todo' in self.browser.title
        assert 'Todo' in self.browser.find_element_by_tag_name('h1').text

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        assert input_box.get_attribute('placeholder') == 'Enter a todo item'

        # She types "Buy tickets to the moon" into a text box (Edith's hobby
        # is travelling)
        edith_input_1 = "Buy tickets to the Moon"
        input_box.send_keys(edith_input_1)
        input_box.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, 'lists/.+')
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy tickets to the Moon" as an item in a to-do list
        self.check_for_row_in_list_table('1: %s' % edith_input_1)

        # There is still a text box inviting her to add another item. She
        # enters "Go to rover driving lesson" (Edith is very methodical)
        input_box = self.browser.find_element_by_id('id_new_item')
        edith_input_2 = "Go to rover driving lesson"
        input_box.send_keys(edith_input_2)
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: %s' % edith_input_1)
        self.check_for_row_in_list_table('2: %s' % edith_input_2)

        # Now a new user, John, logs in

        # use a new browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        # John cannot see Edith's list items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(edith_input_1, page_text)
        self.assertNotIn(edith_input_2, page_text)

        # John adds some items of his own
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)

        # John gets his own url
        john_list_url = self.browser.current_url
        self.assertNotEqual(edith_list_url, john_list_url)
        self.assertRegex(john_list_url, 'lists/.+')

        # John still cannot see Edith's items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(edith_input_1, page_text)
        self.assertNotIn(edith_input_2, page_text)


    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] // 2,
            512,
            delta=5
        )