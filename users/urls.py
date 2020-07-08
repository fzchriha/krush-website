from django.urls import path
from .views import (
	profile,
	view_profile,
	update_friend,
	friends,
	)

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/(?P<pk>\d+)/', view_profile, name='view_profile'),
    path('connect/(?P<operation>.+)/(?P<pk>\d+)/', update_friend, name='update_friend'),
    path('friends/', friends, name='friends'),
]