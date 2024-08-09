from django.urls import path

from . import views

urlpatterns = [
    path("", views.sort_methods, name="sort_methods"),
    path("", views.stores_get, name="stores_get"),
	path("", views.create, name="create")
    ]
