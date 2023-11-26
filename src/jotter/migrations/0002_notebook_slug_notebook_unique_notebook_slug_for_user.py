# Generated by Django 4.2.7 on 2023-11-26 01:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jotter", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notebook",
            name="slug",
            field=models.SlugField(default="my-notes", max_length=100),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="notebook",
            constraint=models.UniqueConstraint(
                fields=("user", "slug"), name="unique_notebook_slug_for_user"
            ),
        ),
    ]
