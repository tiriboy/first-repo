

from urllib import request
from rest_framework.response import Response
from .models import Product,Category, Review
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status
from django.db import models
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import ProductFilter
from .permissions import ProductsAndCategoryPermission
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions

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


class RegisterView(APIView):
    permission_classes =  [permissions.AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token,_= Token.objects.get_or_create(user=user)
        

        return Response({"username":user.username,"key":token.key,"status":status.HTTP_201_CREATED}) 
       
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        token,_= Token.objects.get_or_create(user=user)

        return Response({"username":serializer.validated_data["username"],"key":token.key,"status":status.HTTP_200_OK})

class LogoutView(APIView):
    permission_classes =[permissions.IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"Logout successful"})


