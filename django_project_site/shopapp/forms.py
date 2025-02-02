from django import forms
from django.core import validators
from django.contrib.auth.models import User, Group
from django.forms import ClearableFileInput

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


class MultipleClearableFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleClearableFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


# Implemented forms.ModelForm
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = MultipleImageField()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "user",
            "delivery_address",
            "products",
            "promocode",
        ]
        widgets = {
            "user": forms.RadioSelect(attrs={"placeholder": "Enter user"}),
            "products": forms.CheckboxSelectMultiple(attrs={"rows": 4, "cols": 40}),
            "delivery_address": forms.Textarea(
                attrs={
                    "rows": 4,
                    "cols": 40,
                    "placeholder": "Enter delivery address",
                }
            ),
            "promocode": forms.TextInput(attrs={"placeholder": "Enter promo code"}),
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


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
