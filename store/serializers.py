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


class RegisterSerializer(serializers.ModelSerializer):
      password = serializers.CharField(write_only = True)
      class Meta:
          model = User
          fields = ['username', 'email', 'password']

      def create(self, validated_data):
            user = User.objects.create_user(username=validated_data["username"],email=validated_data["email"],password=validated_data["password"])  
            return user
      

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        user = authenticate( username= data["username"], password=data["password"])
        if not user:
             raise serializers.ValidationError
        data["user"] = user
        return data
                              




    