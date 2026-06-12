from django.contrib import admin
from .models import Category, Product

#registro i modelli del catalogo
admin.site.register(Category)
admin.site.register(Product)