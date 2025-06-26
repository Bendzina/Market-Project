from django.urls import path
from .views import ProductListView, ProductCreateView, ProductAPI, CategoryListView, CategoryDetailView, CategoryApi, BrandsDetailView, BrandsListView, BrandApi, CategoryparamsListView, CategoryparamsApi, CategoryparamsDetailView, ProductparamsListView, ProductparamsDetailView, ProductparamsApi, RegisterView, LoginView, SkuListView, SkuApi, SkuDetailView, ProductSearchApi, LogoutView, ProductImageListView, ProductImageDelete
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProductViewSet, BrandsViewSet, CategoryViewSet, ProductImageUpload, product_page, LoginView
from rest_framework.routers import DefaultRouter
from .views import search_products
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    # Product URLs
    path('products/', ProductListView.as_view(), name='product-list-view'),
    path('products-create/', ProductCreateView.as_view(), name='product-create-view'),
    path('products-api/', ProductAPI.as_view(), name='product-api'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories-api/', CategoryApi.as_view(), name='category-api'),

    # Brand URLs
    path('brands/', BrandsListView.as_view(), name='brand-list'),
    path('brands/<int:pk>/', BrandsDetailView.as_view(), name='brand-detail'),
    path('brands-api/', BrandApi.as_view(), name='brand-api'),
    
    # Catparams URLs
    path('categoryparams/', CategoryparamsListView.as_view(), name='categoryparams-list'),
    path('categoryparams/<int:pk>/', CategoryparamsDetailView.as_view(), name='categoryparams-detail'),
    path('categoryparams-api/', CategoryparamsApi.as_view(), name='categoryparams-api'),

    # Productparams URLs
    path('productparams/', ProductparamsListView.as_view(), name='productparams-list'),
    path('productparams/<int:pk>/', ProductparamsDetailView.as_view(), name='productparams-detail'),
    path('productparams-api/', ProductparamsApi.as_view(), name='productparams-api'),
    
    # SKU URLs
    path('skus/', SkuListView.as_view(), name='sku-list'),
    path('skus/<int:pk>/', SkuDetailView.as_view(), name='sku-detail'),
    path('skus-api/', SkuApi.as_view(), name='sku-api'),
    
    # # Token URLs
    # path('app/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('app/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Authentication endpoints
    path('registrations/', RegisterView.as_view(), name='registrations'),
    path('app/login/', LoginView.as_view(), name='app-login'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Search API
    path('products/search/', ProductSearchApi.as_view(), name='product-search'),

    # Image upload  
    path('products/<int:product_id>/images/', ProductImageUpload.as_view(), name='product-image-upload'),
    path('products/<int:product_id>/images/list/', ProductImageListView.as_view(), name='product-image-list'),
    path('products/images/<int:image_id>/delete/', ProductImageDelete.as_view(), name='product-image-delete'),
    
    path('products-page/', product_page, name='product-html-view'),
    
    # # Login
    # path('login/', LoginView.as_view(), name='login'),


]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# viewset
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'brands', BrandsViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns += router.urls



# http://127.0.0.1:8000/products-list/

