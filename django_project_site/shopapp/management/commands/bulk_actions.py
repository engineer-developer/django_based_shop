from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Product, Order


class Command(BaseCommand):
    """Make bulk actions"""

    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")
        users_qs = User.objects.filter(pk__in=[1, 2, 3])
        users = list(users_qs)
        info = [
            ("Gadget_1", 199, users[0]),
            ("Gadget_2", 299, users[1]),
            ("Gadget_3", 399, users[2]),
        ]
        products = [
            Product(name=name, price=price, created_by=user)
            for name, price, user in info
        ]
        result = Product.objects.bulk_create(products)
        for obj in result:
            print(obj)

        self.stdout.write(self.style.SUCCESS("Done"))
