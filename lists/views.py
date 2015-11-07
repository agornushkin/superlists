# from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse(b'<html><title>Todo lists</title></html>')
# Create your views here.
