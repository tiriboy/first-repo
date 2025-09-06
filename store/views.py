

from urllib import request
from rest_framework.response import Response
from .models import Product,Category, Review
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer,UserSerializer
from rest_framework import status
from django.db import models
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import ProductFilter
from rest_framework import permissions
from django.contrib.auth.models import User

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
 
    serializer_class = ProductSerializer
    lookup_field = 'id'
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price']
    search_fields = ['name', 'description', 'category__name']
    permission_classes = [permissions.IsAuthenticated]


    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().annotate(products_count = models.Count('products'))
    serializer_class = CategorySerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
    
      

    def destroy(self, request, id):
        category = get_object_or_404(Category.objects.all().annotate(products_count = models.Count('products')), id = id)
        if category.products_count > 0:
            return Response({"error": "Category is not empty"}, status=status.HTTP_400_BAD_REQUEST)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

       

class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [permissions.IsAdminUser]
        filter_backends = [SearchFilter, OrderingFilter]
        search_fields = ['username', 'email']
        ordering_fields = ['username'] 
        



