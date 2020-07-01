from django.urls import path
from .views import home_view, CreateCrush, detail_view, tagged
from django.conf.urls import url

url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
