from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Product, Order


class Command(BaseCommand):
    """Make bulk update"""

    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        result = Product.objects.filter(name__contains="Gadget").update(discount=10)
        print(result)

        self.stdout.write(self.style.SUCCESS("Done"))
