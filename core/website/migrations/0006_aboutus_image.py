# Generated by Django 5.2.4 on 2025-07-18 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_remove_aboutus_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutus",
            name="image",
            field=models.ImageField(null=True, upload_to="website/about_us/"),
        ),
    ]
