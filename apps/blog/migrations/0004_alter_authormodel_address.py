# Generated by Django 4.2.1 on 2023-07-25 13:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_remove_authormodel_name_remove_contactmodel_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authormodel",
            name="Address",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]