# Generated by Django 3.2.5 on 2021-08-13 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210813_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='lenght',
            field=models.PositiveIntegerField(default=20),
        ),
    ]
