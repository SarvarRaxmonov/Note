# Generated by Django 4.2.1 on 2023-07-26 15:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0022_alter_viewcountmodel_timestamp"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="AuthorModel",
            new_name="Author",
        ),
        migrations.RenameModel(
            old_name="AuthorOccupationModel",
            new_name="AuthorOccupation",
        ),
        migrations.RenameModel(
            old_name="BlogPostModel",
            new_name="BlogPost",
        ),
        migrations.RenameModel(
            old_name="CategoryModel",
            new_name="Category",
        ),
        migrations.RenameModel(
            old_name="CommentModel",
            new_name="Comment",
        ),
        migrations.RenameModel(
            old_name="ContactModel",
            new_name="Contact",
        ),
        migrations.RenameModel(
            old_name="ReviewModel",
            new_name="Review",
        ),
        migrations.RenameModel(
            old_name="SocialMediaModel",
            new_name="SocialMedia",
        ),
        migrations.RenameModel(
            old_name="TagModel",
            new_name="Tag",
        ),
        migrations.RenameModel(
            old_name="ViewCountModel",
            new_name="ViewCount",
        ),
    ]