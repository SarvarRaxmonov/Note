# Generated by Django 4.2.1 on 2023-07-25 19:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_remove_blogpostmodel_hashtag_blogpostmodel_hashtag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpostmodel",
            name="date_time",
            field=models.DateField(auto_now=True),
        ),
    ]