from unittest import skip

from .base import FunctionalTest


class ValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith go to home page
        self.browser.get(self.server_url)
        # Tries to add an empty item
        self.find_input_box_for_new_item().send_keys('\n')
        # Gets an error
        error = self.find_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")
        # Corrects
        self.find_input_box_for_new_item().send_keys('Buy milk\n')
        # Item is added, no errors
        self.check_for_row_in_list_table('1: Buy milk')
        # Tries to add another empty item
        self.find_input_box_for_new_item().send_keys('\n')
        # Gets an error
        error = self.find_error_element()
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
        error = self.find_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def find_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_errors_disappear_on_input(self):
        # Edith go to home page
        self.browser.get(self.server_url)
        # Adds an empty item which causes an error
        self.find_input_box_for_new_item().send_keys('\n')
        error = self.find_error_element()
        self.assertTrue(error.is_displayed())

        # Starts typing in the box to clear the error
        self.find_input_box_for_new_item().send_keys('a')

        # notices that the error magically disappeared
        self.assertFalse(error.is_displayed())

    def test_errors_disappear_on_click_on_input_box(self):
        # Edith go to home page
        self.browser.get(self.server_url)
        # Adds an empty item which causes an error
        self.find_input_box_for_new_item().send_keys('\n')
        error = self.find_error_element()
        self.assertTrue(error.is_displayed())

        # clicks on the input box to start fixing an error
        self.find_input_box_for_new_item().click()

        # notices that the error magically disappeared
        self.assertFalse(error.is_displayed())



