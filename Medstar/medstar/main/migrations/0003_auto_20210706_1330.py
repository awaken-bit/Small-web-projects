# Generated by Django 3.1.2 on 2021-07-06 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210706_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='patronymic',
            field=models.CharField(default='Ивановичь', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reference',
            name='symptoms',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.symptom'),
        ),
    ]
