from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction


from shopapp.models import Order, Product


class Command(BaseCommand):
    """Create order with products"""

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with products")
        user: User = User.objects.get(username="admin")
        products: Sequence[Product] = Product.objects.only("id").all()
        order, created = Order.objects.get_or_create(
            delivery_address="Nekrasova str., d.55",
            promocode="SUPERSALE2",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Created order {order}")
