from datetime import datetime
from timeit import default_timer

from django.contrib.auth.models import Group, User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views import View

from shopapp.forms import OrderForm, ProductForm, GroupForm
from shopapp.models import Order, Product


def show_greetings(request: HttpRequest) -> HttpResponse:
    """Show greetings for a user."""

    print("INFO:", request.path)
    print("INFO:", request.method)
    print("INFO:", request.headers)
    print("INFO:", request.get_host())
    return HttpResponse(content="<h1>Have a nice day!</h1>")


def show_index(request: HttpRequest) -> HttpResponse:
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
    return render(
        request,
        "shopapp/shop-index.html",
        context=context,
    )


def users_list(request: HttpRequest) -> HttpResponse:
    """Get users list."""

    context = {"users": User.objects.all()}
    return render(request, "shopapp/users-list.html", context=context)


def groups_list(request: HttpRequest) -> HttpResponse:
    """Get groups list."""

    context = {"groups": Group.objects.prefetch_related("permissions").all()}
    return render(
        request,
        "shopapp/groups-list.html",
        context=context,
    )


def products_list(request: HttpRequest) -> HttpResponse:
    """Get products list."""

    context = {
        "products": Product.objects.all(),
    }
    return render(request, "shopapp/products-list.html", context=context)


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


def orders_list(request: HttpRequest) -> HttpResponse:
    """Get orders list."""

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
