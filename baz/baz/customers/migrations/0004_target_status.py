# Generated by Django 3.1.2 on 2020-10-24 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='status',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
