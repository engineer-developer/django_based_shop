from django.contrib import admin
from django.db.models import QuerySet
from django import forms
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.translation import gettext_lazy as _

from shopapp.common import save_csv_products, save_csv_orders, save_json_orders
from shopapp.models import Product, Order, ProductImage
from shopapp.admin_mixins import ExportAsCSVMixin
from shopapp.forms import CSVImportForm, JSONImportForm


@admin.action(description=_("Archive products"))
def mark_archived(
    modeladmin: admin.ModelAdmin,
    request: HttpRequest,
    queryset: QuerySet,
):
    queryset.update(archived=True)


@admin.action(description=_("Unarchive products"))
def mark_unarchived(
    modeladmin: admin.ModelAdmin,
    request: HttpRequest,
    queryset: QuerySet,
):
    queryset.update(archived=False)


class OrderInline(admin.TabularInline):
    model = Product.orders.through
    extra = 1


class ProductInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products_change_list.html"
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
        ProductInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    # readonly_fields = ("price", "discount")
    ordering = ("pk", "name")
    empty_value_display = "---"
    # list_per_page = 2
    search_fields = "name", "description", "price"
    fieldsets = [
        (
            None,
            {
                "fields": ("name", "description"),
            },
        ),
        (
            "Price options",
            {
                "fields": ("price", "discount"),
                "classes": ("wide", "collapse"),
            },
        ),
        (
            "Images",
            {
                "fields": ("preview",),
                "classes": ("wide", "collapse"),
            },
        ),
        (
            "Extra options",
            {
                "fields": ("archived",),
                "classes": ("collapse",),
                "description": "Extra options. Field 'archived' is for soft delete",
            },
        ),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {"form": form}
            return render(request, "admin/csv_form.html", context)
        elif request.method == "POST":
            form = CSVImportForm(request.POST, request.FILES)
            if not form.is_valid():
                context = {"form": form}
                return render(request, "admin/csv_form.html", context, status=400)

            # csv_file = TextIOWrapper(
            #     form.files["csv_file"].file,
            #     encoding=request.encoding,
            # )
            # reader = DictReader(csv_file)
            # products = [Product(**row) for row in reader]
            # Product.objects.bulk_create(products)

            save_csv_products(
                file=form.files["csv_file"].file,
                encoding=request.encoding,
            )

            self.message_user(request, "Successfully imported products from CSV.")
            return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls


# admin.site.register(Product, ProductAdmin)


class OrderProductsInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_change_list.html"
    inlines = [
        OrderProductsInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"rows": 2, "cols": 35}),
        }
    }

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        """Import orders from a CSV file."""

        if request.method == "GET":
            form = CSVImportForm()
            context = {"form": form}
            return render(request, "admin/csv_form.html", context)
        elif request.method == "POST":
            form = CSVImportForm(request.POST, request.FILES)
            if not form.is_valid():
                context = {"form": form}
                return render(request, "admin/csv_form.html", context, status=400)

            save_csv_orders(
                file=form.files["csv_file"].file,
                encoding=request.encoding,
            )

            self.message_user(request, "Successfully imported orders from CSV.")
            return redirect("..")

    def import_json(self, request: HttpRequest) -> HttpResponse:
        """Import orders from a JSON file."""

        if request.method == "GET":
            form = JSONImportForm()
            context = {"form": form}
            return render(request, "admin/json_form.html", context)
        elif request.method == "POST":
            form = JSONImportForm(request.POST, request.FILES)
            if not form.is_valid():
                context = {"form": form}
                return render(request, "admin/json_form.html", context, status=400)

            save_json_orders(
                file=form.files["json_file"].file,
                encoding=request.encoding,
            )

            self.message_user(request, "Successfully imported orders from JSON.")
            return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-orders-csv/",
                self.import_csv,
                name="import_orders_csv",
            ),
            path(
                "import-orders-json/",
                self.import_json,
                name="import_orders_json",
            ),
        ]
        return new_urls + urls
