# Generated by Django 5.1.2 on 2024-12-30 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_productimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='products/images/thumbnails/'),
        ),
    ]
