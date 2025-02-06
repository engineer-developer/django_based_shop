"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""

from csv import DictWriter
import socket
import logging
from datetime import datetime
from timeit import default_timer

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.cache import cache
from django.contrib.auth.models import Group, User
from django.contrib.syndication.views import Feed
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema, OpenApiResponse

from shopapp.forms import GroupForm, OrderForm, ProductForm
from shopapp.models import Order, Product, ProductImage
from shopapp.serializers import ProductSerializer, OrderSerializer
from shopapp.common import save_csv_products

logger = logging.getLogger(__name__)


def show_greetings(request: HttpRequest) -> HttpResponse:
    """Show greetings for a user."""

    print("INFO:", request.path)
    print("INFO:", request.method)
    print("INFO:", request.headers)
    print("INFO:", request.get_host())
    return HttpResponse(content="<h1>Have a nice day!</h1>")


class ShopIndexView(View):

    # @method_decorator(cache_page(60 * 2))
    def get(self, request: HttpRequest) -> HttpResponse:
        """Get index page."""

        products = [
            ("laptop", 1999),
            ("desktop", 2999),
            ("smartphone", 999),
            ("mouse", 99),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "current_date": datetime.now(),
            "items": 3,
        }

        host, aliaslist, ips = socket.gethostbyname_ex(socket.gethostname())
        logger.info(f"Host: {host}")
        logger.info(f"Alias list: {aliaslist}")
        logger.info(f"IP list: {ips}")

        logger.debug("Products for shop index %s", products)
        logger.info("Rendering shop index")

        print("shop index context", context)

        return render(request, "shopapp/shop-index.html", context=context)


def users_list(request: HttpRequest) -> HttpResponse:
    """Get users list."""

    context = {"users": User.objects.all()}
    return render(request, "shopapp/users-list.html", context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Get groups list."""
        context = {
            "groups": Group.objects.prefetch_related("permissions").all(),
            "form": GroupForm(),
        }
        return render(request, "shopapp/groups-list.html", context=context)

    def post(self, request: HttpRequest):
        """Create new group."""
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    """Get product details."""

    template_name = "shopapp/product-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    """Get products list."""

    template_name = "shopapp/products-list.html"
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


class ProductCreateView(CreateView):
    """Create new product.

    Product can create admins or users which have permission
    to create new products.
    """

    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")
    template_name = "shopapp/product_form.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.request.user
        form.instance.created_by = user
        return super().form_valid(form)


# def create_product(request: HttpRequest) -> HttpResponse:
#     """Create a new product."""
#
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data["name"]
#             # price = form.cleaned_data["price"]
#             # description = form.cleaned_data["description"]
#             # Product.objects.create(name=name, price=price, description=description)
#
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#
#     context = {"form": form}
#     return render(request, "shopapp/create-product.html", context)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    """Update product.

    The update can be performed by admins or users which created product
    and have permissions to change product.
    """

    def test_func(self):
        product = self.get_object()
        checking_conditions = (
            self.request.user.has_perm("shopapp.change_product"),
            product.created_by == self.request.user,
        )
        return self.request.user.is_superuser or all(checking_conditions)

    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        images = form.files.getlist("images")
        for image in images:
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductArchiveView(DeleteView):
    """Archive a product."""

    model = Product
    success_url = reverse_lazy("shopapp:products_list")
    template_name_suffix = "_confirm_archive"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductDeleteView(DeleteView):
    """Delete a product."""

    model = Product
    success_url = reverse_lazy("shopapp:products_list")


class ProductsDataExportView(View):
    """Export product data."""

    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        return JsonResponse({"products": products_data})


@extend_schema(description="Product views CRUD.", tags=["Products"])
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный набор CRUD для сущностей товаров
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        print("Hello products list")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one product by ID",
        description="Get product, return 404 if not found",
        responses={
            "200": ProductSerializer,
            "404": OpenApiResponse(
                description="Product not found",
            ),
        },
    )
    def retrieve(self, *args, **kwargs):
        return super(self).retrieve(*args, **kwargs)

    @action(detail=False, methods=["get"])
    def download_csv(self, request: Request):

        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        fields = ["name", "description", "price", "discount"]
        queryset = self.filter_queryset(self.get_queryset()).only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({field: getattr(product, field) for field in fields})

        return response

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser],
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class LatestProductsFeed(Feed):
    """Latest product feed (RSS)"""

    title = "Shop products (latest)"
    description = "Updates on changes and additions new products to shop"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
            Product.objects.select_related("created_by")
            .filter(archived=False)
            .defer("preview")
            .order_by("-created_at")[:6]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return "{}\n{}".format(item.price, item.description)

    def item_link(self, item: Product):
        return item.get_absolute_url()

    def item_pubdate(self, item: Product):
        return item.created_at


class OrderListView(LoginRequiredMixin, ListView):
    """Get orders list.

    Shows orders with at least one product.\n
    Orders list can get only logged-in users.
    """

    # Get all orders with count of products greater then 0
    queryset = (
        Order.objects.select_related("user")
        .prefetch_related("products")
        .annotate(products_count=Count("products"))
        .filter(products_count__gt=0)
        .order_by("pk")
    )
    # model = Order
    context_object_name = "orders"


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    """Get order details.

    Order details can get only users which have permission
    to view order details.
    """

    permission_required = "shopapp.view_order"
    model = Order
    context_object_name = "order"


class OrderCreateView(CreateView):
    """Create a new order."""

    model = Order
    form_class = OrderForm
    # fields = "user", "delivery_address", "products", "promocode"
    success_url = reverse_lazy("shopapp:orders_list")


# def create_order(request: HttpRequest) -> HttpResponse:
#     """Create a new order."""
#
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return redirect(url)
#     else:
#         form = OrderForm()
#
#     context = {"form": form}
#     return render(request, "shopapp/create-order.html", context=context)


class OrderUpdateView(UpdateView):
    """Update an order."""

    model = Order
    form_class = OrderForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    """Delete an order."""

    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrdersExportView(UserPassesTestMixin, View):
    """Export order data."""

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = (
            Order.objects.select_related("user")
            .prefetch_related("products")
            .annotate(products_count=Count("products"))
            .filter(products_count__gt=0)
            .order_by("pk")
            .all()
        )
        orders_data = [
            {
                "id": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.pk,
                "products_id": [
                    product.pk for product in order.products.order_by("pk").all()
                ],
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


@extend_schema(description="Order views CRUD.", tags=["Orders"])
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("products")
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["delivery_address", "promocode"]
    filterset_fields = [
        "delivery_address",
        "promocode",
        "user",
        "products",
    ]
    ordering_fields = [
        "delivery_address",
        "promocode",
        "user",
    ]

    @extend_schema(
        summary="Get list of orders",
        description="Get orders, uses filters, searching and ordering",
        external_docs={
            "url": "http://localhost:8000/en/shop/orders/",
            "description": "Order list",
        },
    )
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Create new order",
        description="Create order by send data in body",
        responses={
            "201": OpenApiResponse(
                description="Order created",
                response=OrderSerializer,
            ),
            "400": OpenApiResponse(description="Bad request"),
        },
    )
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @extend_schema(
        summary="Get order by ID",
        description="Fetch order details by ID",
        responses={
            "200": OrderSerializer,
            "404": OpenApiResponse(description="Order not found"),
        },
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @extend_schema(
        summary="Update order",
        description="Full update order by ID",
        responses={
            "200": OrderSerializer,
            "400": OpenApiResponse(description="Bad request"),
            "404": OpenApiResponse(description="Order not found"),
        },
    )
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @extend_schema(
        summary="Partial update order",
        description="Partial update order by ID",
        responses={
            "200": OrderSerializer,
            "400": OpenApiResponse(description="Bad request"),
            "404": OpenApiResponse(description="Order not found"),
        },
    )
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)

    @extend_schema(
        summary="Delete order",
        description="Delete order with given ID",
        responses={
            "204": OpenApiResponse(description="No response body"),
            "404": OpenApiResponse(description="Order not found"),
        },
    )
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)
