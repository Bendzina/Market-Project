from django.db import models
from django.core.exceptions import ValidationError
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile
from imagekit.cachefiles.backends import Simple
from PIL import Image
import os
from django.conf import settings
from imagekit.models import ImageSpecField



class Store(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Brands(models.Model):
    id = models.BigAutoField(primary_key=True)
    brand = models.CharField(max_length=50)
    
    def __str__(self):
        return self.brand

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    catid = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(null=False)
    brandid = models.ForeignKey(Brands, on_delete=models.CASCADE)


    # New fields for shipping information
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=1, null=False, help_text="Weight in kg")
    length = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False, help_text="Length in cm")
    width = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False, help_text="Width in cm")
    height = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False, help_text="Height in cm")

    storeid = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    def imagescount(self):
        return self.productimage_set.count()

class Sku(models.Model):
    id = models.BigAutoField(primary_key=True)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.productid)



class Productparams(models.Model):
    id = models.BigAutoField(primary_key=True)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)
    skuid = models.ForeignKey(Sku, on_delete=models.CASCADE, null=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)


    def __str__(self):
        return self.key

class Categoryparams(models.Model):
    id = models.BigAutoField(primary_key=True)
    catid = models.ForeignKey(Category, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)

    def __str__(self):
        return self.key
    
# class ProductImage(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='media/products/images/', blank=False, null=False)
#     thumbnail = ProcessedImageField(
#         upload_to='products/images/thumbnails',
#         processors=[ResizeToFill(100, 100)],
#         format='JPEG',
#         options={'quality': 80},
#         blank=True,
#         null=True,
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if self.product.images.count() >= 6:
#             raise ValidationError("You can only upload a maximum of 6 images for a product")
#         super().save(*args, **kwargs)
    

#     def __str__(self):
#         return f"{self.product.name} - Image {self.id}"
        

# class ProductImage(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='products/images/', blank=False, null=False)
#     thumbnail = models.ImageField(upload_to='products/images/thumbnails/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         # Thumbnail-ის გენერაცია Pillow-ის გამოყენებით
#         if self.image and not self.thumbnail:
#             self.generate_thumbnail()

#     def generate_thumbnail(self):
#         image_path = self.image.path
#         thumbnail_path = os.path.join(
#             settings.MEDIA_ROOT,
#             'products/images/thumbnails',
#             os.path.basename(self.image.name)
#         )

#         # Pillow ბიბლიოთეკის გამოყენება თუმბნეილის შესაქმნელად
#         with Image.open(image_path) as img:
#             if img.mode == 'RGBA':
#                 img = img.convert('RGB')
#             img.thumbnail((100, 100))  # თუმბნეილის ზომა
#             img.save(thumbnail_path, format='JPEG')

#         # Thumbnail-ის მითითება მოდელში
#         self.thumbnail = f'products/images/thumbnails/{os.path.basename(self.image.name)}'
#         super().save(update_fields=['thumbnail'])

#     def __str__(self):
#         return f"{self.product.name} - Image {self.id}"
    
class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/', blank=False, null=False)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"
    
    @property
    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else None