# Generated by Django 3.0.5 on 2020-04-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200407_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='has_beneficiary',
            field=models.BooleanField(),
        ),
    ]