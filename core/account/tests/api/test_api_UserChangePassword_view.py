from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from ...api.v1.views import UserChangePassword
from ...api.v1.serializer import ChangePasswordSerializer

User = get_user_model()


class UserChangePasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example123.com',
            password='oldpassword123',
            is_active=True
        )
        self.url = '/accounts/api/v1/change_password/'  # Update with your actual URL
        
        # Generate JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_successful_password_change(self):
        """Test successful password change with valid data"""

        data = {
            "old_password": "oldpassword123",
            "new_password": "newsecurepassword123",
            "new_password1": "newsecurepassword123"
        }
        
        response = self.client.put(
            self.url,
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Your password changed successfully')
        
        # Verify password was actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecurepassword123'))

    def test_password_change_unauthenticated(self):
        """Test password change without authentication"""
        self.client.credentials()  # Remove authentication
        data = {
            "old_password": "oldpassword123",
            "new_password": "newsecurepassword123",
            "new_password1": "newsecurepassword123"
        }
        response = self.client.put(
            self.url,
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_current_password(self):
        """Test with incorrect current password"""
        data = {
            "old_password": "wrongcurrentpassword",
            "new_password": "newsecurepassword123",
            "new_password1": "newsecurepassword123"
        }
        response = self.client.put(
            self.url,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old password', str(response.data["detail"]))

    def test_weak_new_password(self):
        """Test with weak new password"""
        data = {
            "old_password": "oldpassword123",
            "new_password": "123",
            "new_password1": "123"
        }
        
        response = self.client.put(
            self.url,
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('too short', str(response.data))

    def test_missing_required_fields(self):
        """Test with missing required fields"""
        response = self.client.put(
            self.url,
            data={},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
        self.assertIn('old_password', response.data)

    def test_permission_classes(self):
        """Test that view requires authentication"""
        view = UserChangePassword()
        self.assertEqual(view.permission_classes, [IsAuthenticated])

    def test_serializer_class(self):
        """Test that correct serializer is used"""
        view = UserChangePassword()
        self.assertEqual(view.serializer_class, ChangePasswordSerializer)