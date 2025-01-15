from datetime import datetime
from timeit import default_timer

from django.contrib.auth.models import Group, User
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)

from shopapp.forms import OrderForm, ProductForm, GroupForm
from shopapp.models import Order, Product


def show_greetings(request: HttpRequest) -> HttpResponse:
    """Show greetings for a user."""

    print("INFO:", request.path)
    print("INFO:", request.method)
    print("INFO:", request.headers)
    print("INFO:", request.get_host())
    return HttpResponse(content="<h1>Have a nice day!</h1>")


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Get index page."""

        products = [
            ("laptop", 1999),
            ("desktop", 2999),
            ("smartphone", 999),
            ("mouse", 99),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "current_date": datetime.now(),
        }
        return render(request, "shopapp/shop-index.html", context=context)


def users_list(request: HttpRequest) -> HttpResponse:
    """Get users list."""

    context = {"users": User.objects.all()}
    return render(request, "shopapp/users-list.html", context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Get groups list."""
        context = {
            "groups": Group.objects.prefetch_related("permissions").all(),
            "form": GroupForm(),
        }
        return render(request, "shopapp/groups-list.html", context=context)

    def post(self, request: HttpRequest):
        """Create new group."""
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    """Get product details."""

    template_name = "shopapp/product-details.html"
    model = Product
    context_object_name = "product"


class ProductsListView(ListView):
    """Get products list."""

    template_name = "shopapp/products-list.html"
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


class ProductCreateView(CreateView):
    """Create new product.

    Product can create admins or users which have permission
    to create new products.
    """

    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")
    template_name = "shopapp/product_form.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.request.user
        form.instance.created_by = user
        return super().form_valid(form)


# def create_product(request: HttpRequest) -> HttpResponse:
#     """Create a new product."""
#
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data["name"]
#             # price = form.cleaned_data["price"]
#             # description = form.cleaned_data["description"]
#             # Product.objects.create(name=name, price=price, description=description)
#
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#
#     context = {"form": form}
#     return render(request, "shopapp/create-product.html", context)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    """Update product.

    The update can be performed by admins or users which created product
    and have permissions to change product.
    """

    def test_func(self):
        product = self.get_object()
        checking_conditions = (
            self.request.user.has_perm("shopapp.change_product"),
            product.created_by == self.request.user,
        )
        return self.request.user.is_superuser or all(checking_conditions)

    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


class ArchiveProductView(DeleteView):
    """Archive a product."""

    model = Product
    success_url = reverse_lazy("shopapp:products_list")
    template_name_suffix = "_confirm_archive"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductDeleteView(DeleteView):
    """Delete a product."""

    model = Product
    success_url = reverse_lazy("shopapp:products_list")


class ProductsDataExportView(View):
    """Export product data."""

    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


class OrderListView(LoginRequiredMixin, ListView):
    """Get orders list.

    Shows orders with at least one product.\n
    Orders list can get only logged-in users.
    """

    # Get all orders with count of products greater then 0
    queryset = (
        Order.objects.select_related("user")
        .prefetch_related("products")
        .annotate(products_count=Count("products"))
        .filter(products_count__gt=0)
        .order_by("pk")
    )
    # model = Order
    context_object_name = "orders"


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    """Get order details.

    Order details can get only users which have permission
    to view order details.
    """

    permission_required = "shopapp.view_order"
    model = Order
    context_object_name = "order"


class OrderCreateView(CreateView):
    """Create a new order."""

    model = Order
    form_class = OrderForm
    # fields = "user", "delivery_address", "products", "promocode"
    success_url = reverse_lazy("shopapp:orders_list")


# def create_order(request: HttpRequest) -> HttpResponse:
#     """Create a new order."""
#
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return redirect(url)
#     else:
#         form = OrderForm()
#
#     context = {"form": form}
#     return render(request, "shopapp/create-order.html", context=context)


class OrderUpdateView(UpdateView):
    """Update an order."""

    model = Order
    form_class = OrderForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    """Delete an order."""

    model = Order
    success_url = reverse_lazy("shopapp:orders_list")
