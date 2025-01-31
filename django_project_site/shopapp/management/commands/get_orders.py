from django.core.management import BaseCommand

from shopapp.models import Order


class Command(BaseCommand):
    """Get all orders"""

    def handle(self, *args, **options):

        orders = Order.objects.select_related("user").prefetch_related("products")
        for order in orders:
            print(order.pk)
            print("\t", order.delivery_address)
            print("\t", order.promocode)
            print("\t", order.created_at)
            print("\t", order.user)
            print("\t", order.products)
            print("\t", order.receipt)

        self.stdout.write(self.style.SUCCESS("Done"))
