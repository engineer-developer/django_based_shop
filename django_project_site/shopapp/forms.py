from django import forms
from django.core import validators
from django.contrib.auth.models import User, Group

from shopapp.models import Product, Order


# Implemented forms.Form
# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=100000, decimal_places=2)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"rows": 5, "cols": 30}),
#         validators=[
#             validators.RegexValidator(
#                 regex=r"great",
#                 message="Product description must contain word 'great'",
#             )
#         ],
#     )


# Implemented forms.ModelForm
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "description",
            "discount",
        ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "delivery_address",
            "promocode",
            "user",
            "products",
        ]
        widgets = {
            "delivery_address": forms.Textarea(
                attrs={
                    "rows": 4,
                    "cols": 40,
                    "placeholder": "Enter delivery address",
                }
            ),
            "promocode": forms.TextInput(attrs={"placeholder": "Enter promo code"}),
            "user": forms.RadioSelect(attrs={"placeholder": "Enter user"}),
            "products": forms.CheckboxSelectMultiple(attrs={"rows": 4, "cols": 40}),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.all()
        self.fields["products"].queryset = Product.objects.all()


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            "name",
        ]
