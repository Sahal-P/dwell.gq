# Generated by Django 4.1.3 on 2022-11-29 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0018_products_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='offer',
        ),
    ]