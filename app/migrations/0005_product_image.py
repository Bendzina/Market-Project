# Generated by Django 5.1.2 on 2024-12-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_store_product_storeid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/products/images/'),
        ),
    ]
