
from django.urls import path, include
from .views import ProductViewSet,CategoryViewSet, ReviewViewSet,UserViewSet
from rest_framework_nested import routers
from rest_framework_simplejwt import views

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename= 'products')
router.register(r'categories',CategoryViewSet, basename='categories')
router.register(r'users', UserViewSet, basename='users')

products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register(r'reviews', ReviewViewSet, basename='reviews' )



urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('authenticate/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authenticate/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),

]