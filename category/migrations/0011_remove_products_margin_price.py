# Generated by Django 4.1.3 on 2022-11-26 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0010_alter_products_margin_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='margin_price',
        ),
    ]
