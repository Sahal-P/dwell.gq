# Generated by Django 4.1.3 on 2022-11-29 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0020_products_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='offer_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
