from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Cart, CartItem, OrderItem, Order
from app.models import Product, Sku, Productparams
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import CartItemSerializer, OrderSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        # cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            # პროდუქტის მოძიება
            product = Product.objects.get(pk=pk)
            sku = Sku.objects.get(productid=product)

            # კალათის მოძიება ან შექმნა
            cart, created = Cart.objects.get_or_create(user=request.user)

            # CartItem-ის მოძიება ან შექმნა
            cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, sku=sku)

            # shipping information

            cart_item_weight = product.weight
            cart_item_length = product.length
            cart_item_width = product.width
            cart_item_height = product.height

          

            # სტოკის შემოწმება დამატებამდე:
            new_quantity = cart_item.quantity + int(request.data.get("quantity", 1))
            if product.stock < new_quantity:
                return Response({'status': 'error', 'message': 'not enough stock'}, status=400)
            
            if not cart_item_created:
                cart_item.quantity += int(request.data.get("quantity", 1))
            else:
                cart_item.quantity = int(request.data.get("quantity", 1))
            cart_item.save()

            params = request.data.get("params", [])
            for param in params:
                # ვამოწმებთ, არსებობს თუ არა ეს key-value წყვილი ამ პროდუქტისთვის
                existing_param = Productparams.objects.filter(
                    productid=product,
                    skuid=sku,
                    key=param.get("key"),
                    value=param.get("value")
                ).exists()

                # თუ ჩანაწერი არ არსებობს, მხოლოდ მაშინ ვამატებთ
                if not existing_param:
                    Productparams.objects.create(
                        productid=product,
                        skuid=sku,
                        key=param.get("key"),
                        value=param.get("value")
                    )
            serializer = CartItemSerializer(cart_item)
            return Response({
                'status': 'success',
                'message': 'item added successfully',
                'item': serializer.data
            }, status=200)       
        except Product.DoesNotExist:
            return Response({'status': 'error', 'message': 'Product not found'}, status=404)
               
        except Sku.DoesNotExist:
            return Response({'status': 'error', 'message': 'Sku not found for the product'}, status=404)
        
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
        
class UpdateCartItemView(APIView):
    def post(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk)
            quantity = int(request.data.get('quantity'))
            if quantity == 0:
                cart_item.delete()
                return Response({'status': 'success', 'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
            elif quantity <= cart_item.sku.productid.stock:
                cart_item.quantity = quantity
                cart_item.save()
                return Response({'status': 'success', 'message': 'Cart item updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response({'status': 'error', 'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteCartItemView(APIView):
    def post(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk)
            cart_item.delete()
            return Response({'status': 'success', 'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'status': 'error', 'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)



class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'status': 'error', 'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderCreateApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddToCartApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart = cart)

            if not cart_items.exists():
                return Response({
                    "status": "error",
                    "message": "No items in cart"
                }, status=400)
            
         
            total_amount = sum(item.quantity * item.sku.productid.price for item in cart_items)

           

            order = Order.objects.create(
                user=request.user, 
                total_amount=total_amount,
                status='Pending'
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.sku.productid,
                    quantity=item.quantity,
                    price=item.sku.productid.price
                )
            
            cart_items.delete()
            return Response({
                'status': 'success',
                'message': 'Order placed successfully',
                'order_id': order.id,
                'total_amount': total_amount
            }, status=201)
        
        except Cart.DoesNotExist:
            return Response({'status': 'error', 'message': 'Cart not found'}, status=404)
        
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
                

@login_required
def cart_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.quantity * item.sku.productid.price for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': total
    })