# Generated by Django 4.1.3 on 2022-11-25 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_oldcart_date_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='GCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=250)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='oldcart',
            name='cart',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.gcart'),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
