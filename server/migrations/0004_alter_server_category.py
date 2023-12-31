# Generated by Django 4.2.6 on 2023-11-02 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0003_category_icon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="server",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="server_category",
                to="server.category",
            ),
        ),
    ]
