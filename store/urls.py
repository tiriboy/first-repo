
from django.urls import path, include
from .views import ProductViewSet,CategoryViewSet, ReviewViewSet, LoginView, LogoutView, RegisterView
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename= 'products')
router.register(r'categories',CategoryViewSet, basename='categories')

products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register(r'reviews', ReviewViewSet, basename='reviews' )



urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]