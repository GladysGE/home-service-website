# Generated by Django 3.2.10 on 2024-08-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0017_cartdb_discount_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingdb',
            name='Name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
