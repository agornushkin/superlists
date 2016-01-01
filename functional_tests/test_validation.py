from unittest import skip

from .base import FunctionalTest


class ValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith go to home page
        self.browser.get(self.server_url)
        # Tries to add an empty item
        self.find_input_box_for_new_item().send_keys('\n')
        # Gets an error
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        # Corrects
        self.find_input_box_for_new_item().send_keys('Buy milk\n')
        # Item is added, no errors
        self.check_for_row_in_list_table('1: Buy milk')
        # Tries to add another empty item
        self.find_input_box_for_new_item().send_keys('\n')
        # Gets an error
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        # Corrects
        self.find_input_box_for_new_item().send_keys('Make tea\n')
        # Both items are now on the list, no errors
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith go to home page
        self.browser.get(self.server_url)
        # Adds an item
        self.find_input_box_for_new_item().send_keys('Buy an island\n')
        self.check_for_row_in_list_table('1: Buy an island')

        # Accidentally tries to add the same item again
        self.find_input_box_for_new_item().send_keys('Buy an island\n')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list")
