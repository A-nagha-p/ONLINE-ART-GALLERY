from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20)  # Add any additional fields you need


    def __str__(self):
        return self.username

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    theme = models.CharField(max_length=255, blank=True, null=True)
    art_type = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('out-of-stock', 'Out of Stock')])
    product_image = models.ImageField(upload_to='product_images/', max_length=255)

    def __str__(self):
        return self.product_name



class Competition(models.Model):
    competition_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='competition_images/', max_length=255)
    am_pm = models.CharField(max_length=2, choices=[("AM", "AM"), ("PM", "PM")])

    def __str__(self):
        return self.competition_name


