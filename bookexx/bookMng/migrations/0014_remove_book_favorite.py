# Generated by Django 4.1 on 2022-11-30 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0013_book_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='favorite',
        ),
    ]
