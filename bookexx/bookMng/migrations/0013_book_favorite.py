# Generated by Django 4.1 on 2022-11-30 02:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bookMng", "0012_delete_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="favorite",
            field=models.ManyToManyField(
                blank=True, related_name="favorite", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
