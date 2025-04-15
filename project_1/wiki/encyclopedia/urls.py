from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    # "" routnout na /wiki
    path("", views.index, name="index"),
    # "/wiki" main page
    path("wiki/", views.main_page, name="main_page"),
    path("wiki/<str:valid_entry>", views.page, name="page"),
    path("wiki/<str:valid_entry>/edit", views.edit_page, name="edit_page"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("random/", views.random_entry, name="random_entry"),
]
