from django.urls import path

from .views import hello_world_view


app_name = "my_api_app"

urlpatterns = [
    path("hello/", hello_world_view, name="hello"),
]
