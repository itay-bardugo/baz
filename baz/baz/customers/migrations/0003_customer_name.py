# Generated by Django 3.1.2 on 2020-10-23 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20201023_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
