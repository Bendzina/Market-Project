from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, CategoryFilter, BrandsFilter, CategoryparamsFilter, ProductparamsFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from .models import Product, Category, Brands, Categoryparams, Productparams, Sku, ProductImage
from .serializers import ProductSerializer, CategorySerializer, BrandsSerializer, CategoryparamsSerializer, ProductparamsSerializer, RegisterSerializer, SkuSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .permission import BasePermission, SellerPermission
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProductImageSerializer
from django.core.exceptions import ValidationError
from imagekit.cachefiles import ImageCacheFile
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render




# Product Views
class ProductCreateView(CreateAPIView):
    permission_classes = [SellerPermission]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    permission_classes = [SellerPermission]
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Category Views
class CategoryCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class CategoryDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can create category'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Brand Views

class BrandsCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer


class BrandsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BrandsFilter


class BrandsDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer


class BrandApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        brands = Brands.objects.all()
        serializer = BrandsSerializer(brands, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can create brand'}, status=status.HTTP_403_FORBIDDEN)
        serializer = BrandsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Categoryparams Views


class CategoryparamsCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Categoryparams.objects.all()
    serializer_class = CategoryparamsSerializer



class CategoryparamsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Categoryparams.objects.all()
    serializer_class = CategoryparamsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryparamsFilter



class CategoryparamsDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Categoryparams.objects.all()
    serializer_class = CategoryparamsSerializer


class CategoryparamsApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        Categoryparams = Categoryparams.objects.all()
        serializer = CategoryparamsSerializer(Categoryparams, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can create categoryparams'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CategoryparamsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Productparams Views

class ProductparamsCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Productparams.objects.all()
    serializer_class = ProductparamsSerializer


class ProductparamsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Productparams.objects.all()
    serializer_class = ProductparamsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductparamsFilter

class ProductparamsDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Productparams.objects.all()
    serializer_class = ProductparamsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductparamsFilter


class ProductparamsApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        permission_classes = [IsAuthenticated]
        productparams = Productparams.objects.all()
        serializer = ProductparamsSerializer(productparams, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can create productparams'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductparamsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Sku Views

class SkuCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SkuListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SkuDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SkuApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        skus = Sku.objects.all()
        serializer = SkuSerializer(skus, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can create sku'}, status=status.HTTP_403_FORBIDDEN)
        serializer = SkuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#viewset
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer

# რეგისტრაცია
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ლოგინი
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Attempting login for: {username}") 

        user = authenticate(username=username, password=password)
        if user:
            print(f"Login successful for: {username}")
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },status=status.HTTP_200_OK)
        
        print("Invalid credentials")

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            if not refresh_token:
                return Response({"error": "'refresh' key is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Token blacklisted successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
        
    



def search_products(filter_params):

    query = Q()
    for key, value in filter_params.items():
        if value:
            if key == "param_key":  
                query &= Q(productparams__key=value)
            elif key == "param_value":  
                query &= Q(productparams__value=value)
            elif key == "sku":  
                query &= Q(sku__id=value)
            else:
                query &= Q(**{f"{key}__icontains": value})
    
    products = Product.objects.filter(query).distinct()
    return products


class ProductSearchApi(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        filter_params = request.query_params.dict()
        products = search_products(filter_params)
        paginator = PageNumberPagination()
        paginator.page_size = 10  
        result_page = paginator.paginate_queryset(products, request)
        
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)




class ProductImageUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, *args, **kwargs):
        # GET product ID
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # GET files
        images = request.FILES.getlist('images')  # key: 'images'

        if not images:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Product existence check
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Save each image
        for image in images:
            try:
                product_image = ProductImage.objects.create(product=product, image=image)
   
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "id": product_image.id,
            "image": product_image.image.url,
            "thumbnail": product_image.thumbnail.url,  # ეს დამატებული უნდა იყოს
            "created_at": product_image.created_at,
            "product": product.id
        }, status=status.HTTP_201_CREATED)
class ProductImageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductImage.objects.filter(product_id=product_id)
    
class ProductImageDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, image_id, *args, **kwargs):
        try:
            # მოძებნე სურათი მისი ID-ით
            product_image = ProductImage.objects.get(id=image_id)
            product_image.delete()  # წაშალე სურათი
            return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ProductImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)


#front

def product_page(request):
    categories = Category.objects.all()
    products_by_category = {}

    for category in categories:
        products = Product.objects.filter(catid=category)
        products_by_category[category] = products

    return render(request, 'products.html', {
        'products_by_category': products_by_category,
    })
    
    
def login_page(request):
    return render(request, 'login.html')