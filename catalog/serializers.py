from rest_framework import serializers
from catalog.models import Category, Product

class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category = CatagorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title','description','price','stock','is_available','category']