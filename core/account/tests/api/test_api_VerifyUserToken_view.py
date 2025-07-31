from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from rest_framework_simplejwt.settings import api_settings
from datetime import timedelta
from time import sleep
from datetime import datetime, timedelta
import time
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken

from ...api.v1.views import VerifyUserToken  # Update with your actual import path

User = get_user_model()


class VerifyUserTokenTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.inactive_user = User.objects.create_user(
            email='inactive@example.com',
            password='testpass123',
            is_active=False
        )
        self.active_user = User.objects.create_user(
            email='active@example.com',
            password='testpass123',
            is_active=True
        )

    def generate_valid_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def generate_expired_token(self, user):
        """Generate an explicitly expired JWT token"""
        # Create a normal token first to get the base payload
        token = RefreshToken.for_user(user)
        payload = token.access_token.payload
        
        # Manually set expiration to 1 hour ago
        payload['exp'] = int((datetime.utcnow() - timedelta(hours=1)).timestamp())
        
        # Re-encode with modified payload
        expired_token = jwt.encode(
            payload,
            settings.SECRET_KEY,  # Using Django's secret key
            algorithm='HS256'
        )
        return expired_token


    def test_valid_token_activates_inactive_user(self):
        """Test that valid token activates inactive user"""
        token = self.generate_valid_token(self.inactive_user)
        response = self.client.get(f'/accounts/api/v1/verify/{token}/')  # Update with your URL

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'user activated successfully')
        
        # Verify user is now active
        self.inactive_user.refresh_from_db()
        self.assertTrue(self.inactive_user.is_active)

    def test_valid_token_with_active_user(self):
        """Test that valid token with already active user returns proper response"""
        token = self.generate_valid_token(self.active_user)
        response = self.client.get(f'/accounts/api/v1/verify/{token}/')

        self.assertEqual(response.status_code, status.HTTP_208_ALREADY_REPORTED)
        self.assertEqual(response.data['detail'], 'user alrady activated')

    def test_expired_token(self):
        """Test that expired token returns proper error"""
        token = self.generate_expired_token(self.inactive_user)
        response = self.client.get(f'/accounts/api/v1/verify/{token}/')
        
        self.assertEqual(response.status_code, status.HTTP_504_GATEWAY_TIMEOUT)
        self.assertEqual(response.data['detail'], 'Token has expired.')
        
        # Verify user remains inactive
        self.inactive_user.refresh_from_db()
        self.assertFalse(self.inactive_user.is_active)

    def test_invalid_token(self):
        """Test that invalid token returns proper error"""
        invalid_token = "invalid.token.string"
        response = self.client.get(f'/accounts/api/v1/verify/{invalid_token}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid token.')

    # def test_token_without_user_id(self):
    #     """Test that token without user_id returns invalid token error"""
    #     # Create a token without user_id claim
    #     refresh = RefreshToken()
    #     del refresh['user_id']  # Explicitly remove user_id claim
    #     token = str(refresh.access_token)
        
    #     response = self.client.get(f'/accounts/api/v1/verify/{token}/')
        
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['detail'], 'Invalid token.')
        
    # def test_nonexistent_user(self):
    #     """Test that token with non-existent user ID returns invalid token error"""
    #     # Create token for non-existent user
    #     refresh = RefreshToken()
    #     refresh['user_id'] = 99999  # Non-existent user ID
    #     token = str(refresh.access_token)
    #     response = self.client.get(f'/accounts/api/v1/verify/{token}/')

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['detail'], 'Invalid token.')