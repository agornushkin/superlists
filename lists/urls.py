from django.conf.urls import  url
from lists import views


urlpatterns = [
    url(r'^new$', 'lists.views.new_list', name='new_list'),
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
]
