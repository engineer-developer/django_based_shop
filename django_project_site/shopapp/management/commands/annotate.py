from email.policy import default

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count, Sum

from shopapp.models import Product, Order


class Command(BaseCommand):
    """Aggregate function"""

    def handle(self, *args, **options):
        self.stdout.write("Start demo aggregate")

        orders = Order.objects.annotate(
            total=Sum("products__price", default=0),
            products_count=Count("products"),
        ).order_by("total")
        
        for order in orders:
            print(
                f"Order #{order.pk} "
                f"with {order.products_count} "
                f"products summary price {order.total}"
            )

        self.stdout.write(self.style.SUCCESS("Done"))
