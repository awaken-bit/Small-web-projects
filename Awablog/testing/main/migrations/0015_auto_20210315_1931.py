# Generated by Django 3.1.2 on 2021-03-15 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='author_comment',
        ),
    ]