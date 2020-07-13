from django.urls import path, re_path
from .import views

urlpatterns = [
    path(r'index/', views.index),
    path(r'say/', views.say),
    path(r'qs/', views.qs),
    path(r'qb/', views.get_body),
    path(r'set_session/', views.set_session),
    path(r'get_session/', views.get_session),
    path(r'qb/', views.get_body),
    path(r'register/', views.UserView.as_view()),
    path(r'books/', views.BookListView.as_view()),
    re_path(r'books/(\d+)/', views.BookDetailView.as_view()),
    re_path(r'weather/([a-z]+)/(\d{4})/', views.weather),
]
