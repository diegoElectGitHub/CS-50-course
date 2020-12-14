from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.read_page, name="wiki"),
    path("search/", views.search_page, name="site_search"),
    path("new/", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("wiki/", views.random_page, name="random_page")
]
