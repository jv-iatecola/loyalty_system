from django.urls import path

from . import views

urlpatterns = [
    path("", views.sort_methods, name="sort_methods"),
    path("", views.vouchers_get, name="vouchers_get"),
    path("", views.create, name="create"),
    path("", views.delete, name="delete")  
    # path("", views.create, name="create", kwargs={"foo": "baz"})
    ]
