from string import ascii_letters
from random import choices

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.conf import settings

from shopapp.utils import add_two_numbers
from shopapp.models import Product, Order


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="123")
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        self.client.login(username="john", password="123")

        response = self.client.post(
            path=reverse("shopapp:product_create"),
            data={
                "name": self.product_name,
                "price": 123.45,
                "description": "The best mouse",
                "discount": 10,
            },
            follow=True,
        )
        print(response.redirect_chain)
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            "john", email="john@mail.com", password="123"
        )
        cls.product = Product.objects.create(
            name="Product Name",
            price=123.45,
            description="The best mouse",
            created_by=cls.user,
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product_details(self):
        response = self.client.get(
            path=reverse(
                "shopapp:product_details",
                kwargs={"pk": self.product.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            path=reverse(
                "shopapp:product_details",
                kwargs={"pk": self.product.pk},
            )
        )
        print(self.product.name)
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        "groups-fixture.json",
        "users-fixture.json",
        "products-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for count in range(4):
            username = "".join(choices(ascii_letters, k=6))
            User.objects.create_user(username=username, password="123")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        User.objects.all().delete()

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))

        # Checking what status code of response is "200"
        self.assertEqual(response.status_code, 200)

        # Get all unarchived products from database (stored in given fixture)
        products_from_db = Product.objects.filter(archived=False)

        # Get all products from response context
        products_from_context = response.context["products"]

        # Checking what a count of both collections is equal
        self.assertCountEqual(products_from_db, products_from_context)

        # Compare products_from_db with products_from_context in cycle
        for p, p_ in zip(products_from_db, products_from_context):
            self.assertEqual(p.pk, p_.pk)
            self.assertEqual(p.name, p_.name)
            self.assertEqual(p.price, p_.price)

        # Compare both collections through assertQuerySetEqual
        self.assertQuerySetEqual(
            qs=products_from_db,
            values=[p_.pk for p_ in products_from_context],
            transform=lambda prod_qs: prod_qs.pk,
        )

        # Checking what a template with name "shopapp/products-list.html" is being used
        self.assertTemplateUsed(response, "shopapp/products-list.html")


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        "products-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        for count in range(4):
            username = "".join(choices(ascii_letters, k=6))
            User.objects.create_user(username=username, password="123")

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products_export"))
        self.assertEqual(response.status_code, 200)

        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(products_data["products"], expected_data)


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="john", password="123")
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(**self.credentials)

    def tearDown(self):
        self.client.logout()

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailViewTestCase(TestCase):
    fixtures = [
        "products-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="john", password="123")
        permission_view_order = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission_view_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        product = Product.objects.filter(pk=1).first()
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="MSK, Lenina str. 58",
            promocode="SALE200",
        )
        self.order.products.add(product)
        self.order.save()

    def tearDown(self):
        self.order.delete()
        self.client.logout()

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_detail", kwargs={"pk": self.order.pk})
        )

        # Checking what status code of response is "200"
        self.assertEqual(response.status_code, 200)

        # Checking what response is contains delivery_address
        self.assertContains(response, self.order.delivery_address)

        # Checking what response is contains promocode
        self.assertContains(response, self.order.promocode)

        # Checking what a created order and order from response have the same pk
        self.assertEqual(self.order.pk, response.context["object"].pk)
