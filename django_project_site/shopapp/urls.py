from django.urls import path
from shopapp.views import (
    show_greetings,
    show_index,
    groups_list,
    products_list,
    orders_list,
)

app_name = "shopapp"

urlpatterns = [
    path("", show_index, name="index"),
    path("hello/", show_greetings, name="greetings"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", products_list, name="products_list"),
    path("orders/", orders_list, name="orders_list"),
]
