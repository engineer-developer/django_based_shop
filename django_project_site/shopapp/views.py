from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth.models import Group
from timeit import default_timer
from datetime import datetime

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
