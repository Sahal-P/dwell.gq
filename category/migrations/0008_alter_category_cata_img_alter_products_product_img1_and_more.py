# Generated by Django 4.1.3 on 2022-11-25 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0007_products_product_img4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cata_img',
            field=models.ImageField(blank=True, null=True, upload_to='imgs/category_img'),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_img1',
            field=models.ImageField(blank=True, null=True, upload_to='imgs/product_img'),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_img2',
            field=models.ImageField(blank=True, null=True, upload_to='imgs/product_img'),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_img3',
            field=models.ImageField(blank=True, null=True, upload_to='imgs/product_img'),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_img4',
            field=models.ImageField(blank=True, null=True, upload_to='imgs/product_img'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='Sub_img',
            field=models.ImageField(blank=True, null=True, upload_to='imgs/sub_category_img'),
        ),
    ]