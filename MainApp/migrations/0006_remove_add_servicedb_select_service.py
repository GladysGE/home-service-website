# Generated by Django 3.2.10 on 2024-06-27 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0005_add_servicedb_select_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='add_servicedb',
            name='Select_Service',
        ),
    ]
