from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import Group
from timeit import default_timer
from datetime import datetime

from shopapp.forms import ProductForm
from shopapp.models import Product, Order


def show_greetings(request: HttpRequest):
    print("INFO:", request.path)
    print("INFO:", request.method)
    print("INFO:", request.headers)
    print("INFO:", request.get_host())
    return HttpResponse(content="<h1>Have a nice day!</h1>")


def show_index(request: HttpRequest):
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


def groups_list(request: HttpRequest):
    context = {"groups": Group.objects.prefetch_related("permissions").all()}
    return render(
        request,
        "shopapp/groups-list.html",
        context=context,
    )


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(
        request,
        "shopapp/products-list.html",
        context,
    )


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

    return render(
        request,
        "shopapp/create-product.html",
        context,
    )


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user")
        .prefetch_related("products")
        .all(),
    }
    return render(
        request,
        "shopapp/orders-list.html",
        context,
    )
