from django.urls import path
from shopapp.views import show_greetings, show_index

app_name = "shopapp"

urlpatterns = [
    path("", show_index, name="index"),
    path("hello/", show_greetings, name="greetings"),
]
