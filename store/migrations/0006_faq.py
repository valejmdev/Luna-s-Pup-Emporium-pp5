# Generated by Django 5.1 on 2024-08-30 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_product_sale_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('category', models.CharField(choices=[('General', 'General'), ('Product-Specific', 'Product-Specific'), ('Order and Shipping', 'Order and Shipping'), ('Returns and Exchanges', 'Returns and Exchanges'), ('Care and Maintenance', 'Care and Maintenance')], max_length=100)),
            ],
        ),
    ]
