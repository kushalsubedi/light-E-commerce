# Generated by Django 4.2 on 2024-01-19 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_rename_items_order_products_remove_order_ordered'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
