from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count

from shopapp.models import Product, Order


class Command(BaseCommand):
    """Aggregate function"""

    def handle(self, *args, **options):
        self.stdout.write("Start demo aggregate")

        result = Product.objects.filter(
            name__contains="Gadget",
        ).aggregate(
            Avg("price"),
            Max("price"),
            min_price=Min("price"),
            count=Count("id"),
        )
        print(result)

        self.stdout.write(self.style.SUCCESS("Done"))
