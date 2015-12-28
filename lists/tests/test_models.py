from django.test import TestCase
from django.forms.models import ValidationError

from ..models import Item, List


class ItemAndListModelsUnitTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'First (ever) item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Second item'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(list_, saved_list)

        all_items = Item.objects.all()
        assert all_items.count() == 2

        first_saved_item, second_saved_item = all_items
        assert first_saved_item.text == 'First (ever) item'
        self.assertEqual(first_saved_item.list, list_)
        assert second_saved_item.text == 'Second item'
        self.assertEqual(second_saved_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()