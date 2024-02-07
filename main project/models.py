from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20)
    phone = models.CharField(max_length=10, null=True, blank=True)
      


    def __str__(self):
        return self.username


User = get_user_model()
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    theme = models.CharField(max_length=255, blank=True, null=True)
    art_type = models.CharField(max_length=255)
    # quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('out-of-stock', 'Out of Stock')])
    product_image = models.ImageField(upload_to='product_images/', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.product_name



class Competition(models.Model):
    competition_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='competition_images/', max_length=255)
    am_pm = models.CharField(max_length=2, choices=[("AM", "AM"), ("PM", "PM")])
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.competition_name






class Blog(models.Model):
    title = models.CharField(max_length=255)
    publishingDate = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'artist'})

    def __str__(self):
        return self.title



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)  # Remove choices
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} - {self.date}"
