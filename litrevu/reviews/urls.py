from django.urls import path
from . import views
from reviews.views import redirect_to_feed

urlpatterns = [
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:ticket_id>/review/create/', views.create_review, name='create_review'),

    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),

    path('ticket/review/create/', views.create_ticket_and_review, name='create_ticket_and_review'),

    path('feed/', views.feed, name='feed'),
    path('', redirect_to_feed, name='redirect_to_feed'),

    path('users/search/', views.search_users, name='search_users'),

]
