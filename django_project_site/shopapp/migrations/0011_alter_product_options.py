# Generated by Django 5.1.5 on 2025-01-26 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0010_productimage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["name"],
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
    ]
