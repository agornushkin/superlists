from django.test import TestCase
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse

from .views import home_page
# Create your tests here.


class HomePageTest(TestCase):

    def test_root_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_has_some_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        assert expected_html == response.content.decode()

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        assert 'A new list item' in response.content.decode()

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )
        assert expected_html == response.content.decode()