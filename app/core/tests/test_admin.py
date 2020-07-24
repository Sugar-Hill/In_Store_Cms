from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_admin_employee(
            email='nipsy@marathon.com',
            password='Password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_employee(
            email='posty@postmalone.com',
            password='Password123',
            full_name='Post Malone'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.full_name)
        self.assertContains(response, self.user.email)
