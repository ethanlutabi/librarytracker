from django.urls import path
from . import views

urlpatterns = [
    path('', views.bool_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name = 'book_detail'),
    path('book/new/', views.book_create, name='book_create'),
    path('book/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:book_id>/delete/', views.book_delete, name='book_delete'),
]