from django.contrib import admin
from .models import CustomUser  # Import your model

admin.site.register(CustomUser)  # Register your model with the admin interface
