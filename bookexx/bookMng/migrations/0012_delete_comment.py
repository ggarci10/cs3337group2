# Generated by Django 4.1 on 2022-11-30 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bookMng", "0011_remove_comment_parent_alter_comment_commentpost_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="Comment",),
    ]
