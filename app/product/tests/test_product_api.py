from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from product.serializers import ProductSerializer

PRODUCTS_URL = reverse('product:product-list')


class PublicProductsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test the login is required for retrieving products"""
        response = self.client.get(PRODUCTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# Test to make sure that only superusers can create products
class PrivateProductsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_employee(
            'test@testing.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test  retrieving tags"""
        Product.objects.create(
            employee=self.user,
            name='UNDER ARMOUR MENS HOVR SONIC',
            price=120.99,
        )

        Product.objects.create(
            employee=self.user,
            name='NIKE MENS ZOOM WINFLO 7',
            price=12.99,
        )

        response = self.client.get(PRODUCTS_URL)

        products = Product.objects.all().order_by('-name')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
