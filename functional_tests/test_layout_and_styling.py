from .base import FunctionalTest


class LayOutTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        input_box = self.find_input_box_for_new_item()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] // 2,
            512,
            delta=5
        )