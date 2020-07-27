from rest_framework import serializers

from core.models import Order
from product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for product objects"""

    class Meta:
        model = Order
        fields = ('id', 'products', 'date_ordered',
                  'is_fulfilled', 'is_completed')
        read_only_fields = ('id',)

    products = ProductSerializer(many=True, read_only=True)
