from django.urls import path, re_path
from .views import (
	register,
	users_list, 
	profile_view, 
	send_friend_request, 
	cancel_friend_request,
	accept_friend_request,
	delete_friend_request,
	profile,
	settings
	)

urlpatterns = [
	path('friends/', users_list, name='users_list'),
	path('(?P<pk>\d+)/', profile_view, name='profile_view'),
	path('register/', register, name='register'),
    re_path(r'^profile$', profile, name='profile'),
    re_path(r'friends/friend-request/send/(?P<id>[\w-]+)/$', send_friend_request),
    re_path(r'^friends/friend-request/cancel/(?P<id>[\w-]+)/$', cancel_friend_request),
    re_path(r'^friends/friend-request/accept/(?P<id>[\w-]+)/$', accept_friend_request),
    re_path(r'^friends/friend-request/delete/(?P<id>[\w-]+)/$', delete_friend_request),
    # path('settings/', settings, name='settings'),
]
