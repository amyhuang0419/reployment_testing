from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.mainpage),
    path('logout', views.logout),
    path('books/create', views.create_book),
    path('books/<int:book_id>', views.display_book),
    path('books/<int:book_id>/update', views.update),
    path('books/<int:book_id>/delete', views.delete),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('all_fav', views.all_fav)
]