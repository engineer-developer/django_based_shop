# Generated by Django 5.1.5 on 2025-02-03 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogapp", "0004_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="pub_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
