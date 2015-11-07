from django.test import TestCase
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
        assert isinstance(response, HttpResponse)
        assert response.content.startswith(b'<html>')
        assert b'<title>Todo lists</title>' in response.content
        assert response.content.endswith(b'</html>')
