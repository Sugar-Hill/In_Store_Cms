from rest_framework import serializers

from core.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image', 'price', 'stock')
        read_only_fields = ('id',)
