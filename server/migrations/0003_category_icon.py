# Generated by Django 4.2.6 on 2023-11-01 06:54

from django.db import migrations, models
import server.models


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0002_alter_server_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.FileField(
                blank=True, null=True, upload_to=server.models.category_icon_upload_path
            ),
        ),
    ]
