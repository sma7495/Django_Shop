# Generated by Django 5.2.4 on 2025-07-18 05:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutUs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slogan", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("image", models.ImageField(upload_to="website/about_us/")),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("updated_date", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "About Us",
                "verbose_name_plural": "About Us",
            },
        ),
    ]
