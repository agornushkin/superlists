from django.test import TestCase
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.utils.html import escape

from ..views import home_page
from ..models import Item, List


class HomePageTest(TestCase):

    def test_root_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_has_some_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        assert expected_html == response.content.decode()


class NewListTest(TestCase):

    def test_saving_a_post_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new list item'

    def test_home_page_redirects_after_posts(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'},
            follow=True
        )
        self.assertRedirects(response, '/lists/1/')

    def test_home_page_returns_error_on_saving_empty_items(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_empty_list_items_are_not_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_list_page_returns_error_on_saving_empty_items(self):
        list_ = List.objects.create()
        response = self.client.post('/lists/{}/'.format(list_.id), data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


class ListViewTest(TestCase):

    def test_list_template_used(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id), follow=True)
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        item_1 = Item.objects.create(text='First item', list=list_)
        item_2 = Item.objects.create(text='Second item', list=list_)

        response = self.client.get('/lists/{}/'.format(list_.id), follow=True)

        self.assertContains(response, item_1.text)
        self.assertContains(response, item_2.text)

    def test_displays_only_items_for_this_list(self):
        list_1 = List.objects.create()
        list_1_item = Item.objects.create(text='Correct list item1', list=list_1)
        list_1_item_2 = Item.objects.create(text='Correct list item2', list=list_1)

        list_2 = List.objects.create()
        list_2_item = Item.objects.create(text='Other list item1', list=list_2)
        list_2_item_2 = Item.objects.create(text='Other list item2', list=list_2)

        response = self.client.get('/lists/{}/'.format(list_1.id))

        self.assertContains(response, list_1_item.text)
        self.assertContains(response, list_1_item_2.text)

        self.assertNotContains(response, list_2_item)
        self.assertNotContains(response, list_2_item_2.text)

    def test_passes_correct_list_object_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_new_item_to_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'item_text': 'A new item to existing list'},
            follow=True,
        )
        self.assertEquals(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEquals(new_item.text, 'A new item to existing list')
        self.assertEquals(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'item_text': 'A new item to existing list'},
            follow=True,
        )
        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))
