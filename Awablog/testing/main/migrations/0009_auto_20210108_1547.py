# Generated by Django 3.1.2 on 2021-01-08 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210105_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='blog',
        ),
        migrations.AddField(
            model_name='entry',
            name='blog',
            field=models.ManyToManyField(to='main.Blog'),
        ),
    ]