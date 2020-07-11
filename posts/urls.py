from django.urls import path
from .views import home_view, CreateCrush, detail_view, tagged


#posts
path('crush/', home_view, name='crush'),
path('crush/create/', CreateCrush, name="create-crush"),
path('post/<slug:slug>/', detail_view, name="detail"),
path('tag/<slug:slug>/', tagged, name="tagged"),

