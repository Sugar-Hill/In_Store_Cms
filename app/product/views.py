from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter

from product.pagination import ProductPageNumberPagination

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
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'name'
    filter_backends = [SearchFilter]
    search_fields = ['name']
    pagination_class = ProductPageNumberPagination

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(employee=self.request.user)
