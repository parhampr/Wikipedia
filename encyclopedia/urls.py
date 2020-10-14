from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.WikiPage, name = "wikipage"),
    path("random/", views.random_page, name="random"),
    path("Newpage/",views.newpage, name="newpage"),
    path("wiki/<str:name>/Edit_page/",views.edit_page, name="Edit_page"),
    path("wiki/search/",views.search, name="search")
]
