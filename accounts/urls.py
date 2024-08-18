from django.urls import path

from . import views

urlpatterns = [
    path("validate/<str:hashed_data>", views.validate, name="validate"),
    path("resend_email", views.resend_email, name="resend_email"),
	path("create", views.create, name="create"),
    path("verify", views.verify, name="verify"),
    path("login", views.login, name="login"),
    path("patch", views.patch, name="patch"),
    path("put", views.put, name="put")
]
