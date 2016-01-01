from django.shortcuts import render, redirect
from django.forms.models import ValidationError

from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
            item.save()
        except ValidationError as exc:
            item.delete()
            return render(request, 'list.html', context={'error': "You can't have an empty list item", 'list': list_})
        else:
            return redirect(list_)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError as exc:
        list_.delete()
        return render(request, 'home.html', context={'error': "You can't have an empty list item"})
    # return redirect('/lists/{}'.format(list_.id))
    return redirect(list_)
