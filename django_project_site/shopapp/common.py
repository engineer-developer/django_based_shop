from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User

from shopapp.models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        buffer=file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)
    products = [Product(**row) for row in reader]
    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        buffer=file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    new_orders = []
    for row in reader:
        order = Order(
            delivery_address=row["delivery_address"],
            promocode=row["promocode"],
            user=User.objects.get(pk=row["user"]),
        )
        order.save()
        products_ids = row["products"].split(" ")
        order_products = Product.objects.filter(pk__in=products_ids)
        order.products.set(order_products)
        new_orders.append(order)

    return new_orders
