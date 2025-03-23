from . import views
from django.urls import path


urlpatterns = [
    path("", views.home, name="app"),
    path("home/", views.read_data, name="read_data"),
    path("predict/", views.model, name="predict"),
    path("contactus/", views.contactus, name="contactus"),
]
