# Generated by Django 4.2.1 on 2023-07-26 12:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0017_remove_blogpostmodel_created"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blogpostmodel",
            old_name="date_time",
            new_name="created",
        ),
    ]