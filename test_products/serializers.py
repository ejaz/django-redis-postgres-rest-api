from rest_framework import serializers 
from test_products.models import Product
 
 
class ProductSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'published')