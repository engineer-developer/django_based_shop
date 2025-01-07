from datetime import datetime
from timeit import default_timer

from django.contrib.auth.models import Group, User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from shopapp.forms import OrderForm, ProductForm, GroupForm
from shopapp.models import Order, Product


def show_greetings(request: HttpRequest) -> HttpResponse:
    """Show greetings for a user."""

    print("INFO:", request.path)
    print("INFO:", request.method)
    print("INFO:", request.headers)
    print("INFO:", request.get_host())
    return HttpResponse(content="<h1>Have a nice day!</h1>")


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Get index page."""

        products = [
            ("laptop", 1999),
            ("desctop", 2999),
            ("smartphone", 999),
            ("mouse", 99),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "current_date": datetime.now(),
        }
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
    model = Product
    context_object_name = "product"


class ProductsListView(ListView):
    """Get products list."""

    template_name = "shopapp/products-list.html"
    model = Product
    context_object_name = "products"


def create_product(request: HttpRequest) -> HttpResponse:
    """Create a new product."""

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data["name"]
            # price = form.cleaned_data["price"]
            # description = form.cleaned_data["description"]
            # Product.objects.create(name=name, price=price, description=description)

            # Product.objects.create(**form.cleaned_data)
            form.save()

            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "shopapp/create-product.html", context)


class OrderListView(ListView):
    """Get order list."""

    queryset = Order.objects.select_related("user").prefetch_related("products")
    context_object_name = "orders"

    context = {
        "orders": Order.objects.select_related("user")
        .prefetch_related("products")
        .all(),
    }
    return render(request, "shopapp/orders-list.html", context)


def create_order(request: HttpRequest) -> HttpResponse:
    """Create a new order."""

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()

    context = {"form": form}
    return render(request, "shopapp/create-order.html", context=context)
