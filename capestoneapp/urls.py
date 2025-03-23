from . import views
from django.urls import path


urlpatterns = [path("", views.read_data, name="read_data")]
