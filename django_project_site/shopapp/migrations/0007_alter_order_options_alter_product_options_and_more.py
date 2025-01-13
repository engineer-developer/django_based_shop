# Generated by Django 5.1.4 on 2025-01-12 14:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0006_order_products"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["created_at"]},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="product",
            name="created_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
