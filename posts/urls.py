from django.urls import path
from .views import (
	crush,
	tagged,
	statistics,
	CreateCrush, 
	PostUpdateView, 
	PostDeleteView, 
	PostDetailView
	)

urlpatterns = [
	path('crush/', crush, name='crush'),
	path('crush/create/', CreateCrush, name="create-crush"),
	path('crush/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
	path('crush/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	# path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('tag/<slug:slug>/', tagged, name="tagged"),
	path('crush/statistics', statistics, name='statistics'),

]
