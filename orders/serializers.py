from rest_framework import serializers
from .models import CartItem, Cart, OrderItem, Order
from app.models import Product, Sku, Productparams
from app.serializers import ProductparamsSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='sku.productid.name', read_only=True)
    product_price = serializers.DecimalField(source='sku.productid.price', max_digits=10, decimal_places=2)
    sku_id = serializers.IntegerField(source='sku.id', read_only=True)
    total_price = serializers.SerializerMethodField()
    # product_params = ProductparamsSerializer(source='sku.productid.productparams_set', many=True, read_only=True)

    # class Meta:
    #     model = CartItem
    #     fields = ['id', 'sku_id', 'product_name', 'quantity', 'product_price', 'total_price', 'product_params']

    # def get_total_price(self, obj):
    #     return obj.sku.productid.price * obj.quantity

    product_params = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'sku_id', 'product_name', 'product_price', 'quantity', 'total_price', 'product_params']

    def get_total_price(self, obj):
        return obj.sku.productid.price * obj.quantity

    def get_product_params(self, obj):
        params = Productparams.objects.filter(productid=obj.sku.productid)
        return [{'key': param.key, 'value': param.value} for param in params]

class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'items', 'total_amount']

    def get_total_amount(self, obj):
        return sum(item.sku.productid.price * item.quantity for item in obj.cartitem_set.all())
    
class OrderItemSerializer(serializers.ModelSerializer):
    Product_name = serializers.CharField(source='product_name')
    # user_id = serializers.IntegerField(source='user.id', read_only=True)
    # items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id',  'Product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source= 'user_id', read_only=True)
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_amount', 'status', 'created_at', 'order_items']





# ///////////ახალი დამატებული
class ProductFilterSerializer(serializers.Serializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    category = serializers.CharField(max_length=255, required=False)