from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@testing.com', password='password'):
    """Create a sample user"""
    return get_user_model().objects.create_employee(email, password)


class ModelTests(TestCase):
    """Testing the models"""

    def test_create_user_with_email_and_password(self):
        """Test creating a user with a username and password"""
        email = 'monkeydluffy@onepiece.com'
        password = 'TestPassword123'
        user = get_user_model().objects.create_employee(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'ichigo@BLEACH.com'
        password = 'TestPassword123'
        user = get_user_model().objects.create_employee(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_employee(None, 'test123')

    def test_create_new_admin_employee(self):
        """Test creating a new admin employee"""
        email = 'rick@rickandmorty.com'
        password = 'I<3Morty'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_product_string(self):
        """Test the product string representation"""
        product = models.Product.objects.create(
            employee=sample_user(),
            name='Nike Air Zoom',
            description='Got a need for speed?',
            price=12.99,
            stock=100,
        )

        self.assertEqual(str(product), product.name)

    @patch('uuid.uuid4')
    def test_product_file_name_uuid(self, mock_uuid):
        """Test that the image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'image.jpg')

        exp_path = f'uploads/product/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
