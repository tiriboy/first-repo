from rest_framework import serializers
from .models import Product, Category, Review
from decimal import Decimal
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields= ['id', 'name', 'description', 'products_count']

    products_count=serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'name', 'description', 'price', 'price_after_tax', 'category']
   
    price_after_tax=serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product:Product):
        tax_rate=0.35
        additional_pay=Decimal(tax_rate)*product.price
        return product.price + additional_pay
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','product','reviewer_name','content', 'date'] 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email"]    
                              




    