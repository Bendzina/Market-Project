# Generated by Django 5.1.2 on 2024-12-26 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_productimage_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='media/products/images/'),
        ),
    ]