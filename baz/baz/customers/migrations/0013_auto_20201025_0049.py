# Generated by Django 3.1.2 on 2020-10-25 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0012_auto_20201025_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='signature',
            field=models.CharField(db_index=True, default='ea94caa367ec419aae272f7293cc665a', max_length=255),
        ),
    ]