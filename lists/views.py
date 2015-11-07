from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return render(request, 'home.html')
    return HttpResponse(b'<html><title>Todo lists</title></html>')
# Create your views here.
