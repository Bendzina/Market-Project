from rest_framework import serializers
from .models import Product, Category, Brands, Categoryparams, Productparams, Sku, ProductImage
from django.contrib.auth.models import User

# for images 


class ProductImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = '__all__'

    def get_thumbnail(self, obj):
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            try:
                return obj.thumbnail.url
            except FileNotFoundError:
                return None  # ან placeholder სურათის URL
        return None

class ProductparamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productparams
 
        fields = '__all__'




class SkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sku
        exclude = ['productid']     
        

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    params = ProductparamsSerializer(many=True, write_only=True, required=False)
    sku = SkuSerializer(write_only=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        params_data = validated_data.pop('params', [])
        sku_data = validated_data.pop('sku', None)
        product = Product.objects.create(**validated_data)

        # Product Params შექმნა
        for param in params_data:
            Productparams.objects.create(product=product, **param)

        # SKU შექმნა
        if sku_data:
            Sku.objects.create(productid=product, **sku_data)

        return product


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField() 
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']  # აქ subcategories დამატებულია

    def get_subcategories(self, obj):
        children = obj.subcategories.all()
        return CategorySerializer(children, many=True).data

class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ['id', 'brand']


class CategoryparamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoryparams
        fields = '__all__'
        


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

