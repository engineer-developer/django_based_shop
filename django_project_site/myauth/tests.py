from django.test import TestCase
from django.urls import reverse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse("myauth:cookie_get"))
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertContains(response, "Cookie with key")


class FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse("myauth:foo_bar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")
        expected_data = {"foo": "bar", "spam": "eggs"}
        self.assertJSONEqual(response.content, expected_data)
        self.assertEqual(response.json(), expected_data)
