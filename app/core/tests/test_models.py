from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test our model"""

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
        user = get_user_model().objects.create_admin_employee(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
