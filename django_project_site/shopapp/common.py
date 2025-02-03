from csv import DictReader
from io import TextIOWrapper

from shopapp.models import Product


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        buffer=file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)
    products = [Product(**row) for row in reader]
    Product.objects.bulk_create(products)
    return products
