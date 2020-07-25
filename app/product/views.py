from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Product

from product import serializers


# Create your views here.
class ProductViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """Manage products in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(employee=self.request.user)
