from rest_framework import serializers
from .models import Product, Category, Brands, Categoryparams, Productparams, Sku, ProductImage
from django.contrib.auth.models import User

# for images 


class ProductImageSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ['id', 'brand']


class CategoryparamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoryparams
        fields = '__all__'
        

class ProductparamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productparams
        fields = '__all__'

class SkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sku
        fields = ['id', 'productid']

# რეგისტრაცია

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

