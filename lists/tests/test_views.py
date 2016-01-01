from django.test import TestCase
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.utils.html import escape

from ..views import home_page
from ..models import Item, List
from ..forms import ItemForm, EMPTY_ITEM_ERROR


class HomePageTest(TestCase):
    maxDiff = None

    def test_home_page_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_saving_a_post_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )
        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new list item'

    def test_home_page_redirects_after_posts(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'},
            follow=True
        )
        self.assertRedirects(response, '/lists/1/')

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_empty_list_items_are_not_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_list_page_returns_error_on_saving_empty_items(self):
        list_ = List.objects.create()
        response = self.client.post('/lists/{}/'.format(list_.id), data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        response = self.client.post('/lists/{}/'.format(list_.id), data={'text': ''})
        return response

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
            data={'text': 'A new item to existing list'},
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
            data={'text': 'A new item to existing list'},
            follow=True,
        )
        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_saves_nothing_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_temlpate(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_displays_error_message(self):
        response = self.post_invalid_input()
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

