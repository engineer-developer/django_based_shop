from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Product


class Command(BaseCommand):
    """Get definite fields"""

    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")

        products_values = Product.objects.values("pk", "name")
        for p_values in products_values:
            print(p_values)

        self.stdout.write(f"Done")
