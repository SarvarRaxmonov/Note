# Generated by Django 4.2.1 on 2023-07-26 13:46

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0019_remove_blogpostmodel_view_count_viewcountmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpostmodel",
            name="text",
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]