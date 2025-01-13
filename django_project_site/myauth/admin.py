from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from myauth.models import Profile
from shopapp.models import Product


class ProfileInline(admin.StackedInline):
    model = Profile


class ProductsInline(admin.StackedInline):
    model = Product
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (
        ProfileInline,
        ProductsInline,
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
