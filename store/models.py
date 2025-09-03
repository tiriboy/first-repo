from django.db import models



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')


    class Meta:
     def __str__(self):
          return self.name
     

class Review(models.Model):  
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,related_name= 'reviews')
    reviewer_name = models.CharField(max_length=100)
    content = models.TextField() 
    date = models.DateTimeField(auto_now=True)  