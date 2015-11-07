import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8000')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

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
        user_input_1 = "Buy tickets to the Moon"
        input_box.send_keys(user_input_1)
        input_box.send_keys(Keys.ENTER)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy tickets to the Moon" as an item in a to-do list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        assert any(row.text == user_input_1 for row in rows), "A new todo item did not appear in the table"
        # There is still a text box inviting her to add another item. She
        # enters "Go to rover driving lesson" (Edith is very methodical)
        user_input_2 = "Go to rover driving lesson"

        # The page updates again, and now shows both items on her list
        self.fail("Finish the test")
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')
