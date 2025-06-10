from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.view_entry, name="view"),
    path("search/", views.search, name="search")
]
