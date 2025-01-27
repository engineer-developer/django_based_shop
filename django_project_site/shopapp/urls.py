from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from shopapp.views import (
    show_greetings,
    # create_product,
    # create_order,
    users_list,
    ShopIndexView,
    GroupsListView,
    ProductDetailsView,
    ProductsListView,
    OrderListView,
    OrderDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductArchiveView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    ProductsDataExportView,
    OrdersExportView,
    ProductViewSet,
)

app_name = "shopapp"

router = DefaultRouter()
router.register("products", ProductViewSet)


urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(router.urls)),
    path("hello/", show_greetings, name="greetings"),
    path("users/", users_list, name="users_list"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="products_export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "products/<int:pk>/archive/",
        ProductArchiveView.as_view(),
        name="product_archive",
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),
    path("orders/create", OrderCreateView.as_view(), name="order_create"),
    # path("orders/create", create_order, name="create_order"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_detail"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]
