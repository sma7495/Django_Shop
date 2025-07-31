from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from ...api.v1.views import CustomTokenObtainPairView
from ...api.v1.serializer import CustomTokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/accounts/api/v1/token/'  # Update with your actual URL
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_active = True,
            # Add any other required fields
        )
        self.inactive_user = User.objects.create_user(
            email='test2@example.com',
            password='testpass123',
            is_active = False,
            # Add any other required fields
        )

    def test_successful_token_obtain(self):
        """Test successful token generation with valid credentials"""
        response = self.client.post(
            self.url,
            data={
                'email': 'test@example.com',
                'password': 'testpass123'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Verify access token is valid
        access_token = response.data['access']
        decoded_token = AccessToken(access_token)
        self.assertEqual(decoded_token['user_id'], self.user.id)

    def test_inactive_user_credentials(self):
        """Test with invalid credentials"""
        response = self.client.post(
            self.url,
            data={
                'email': 'test2@example.com',
                'password': 'testpass123'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(
            str(response.data['detail']),
            'No active account found with the given credentials'
        )

    def test_invalid_credentials(self):
        """Test with invalid credentials"""
        response = self.client.post(
            self.url,
            data={
                'email': 'test@example.com',
                'password': 'wrongpassword'
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(
            str(response.data['detail']),
            'No active account found with the given credentials'
        )

    def test_missing_credentials(self):
        """Test with missing required fields"""
        response = self.client.post(
            self.url,
            data={},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

    def test_custom_claims_in_token(self):
        """Test if custom claims are included in the token"""
        # Assuming your CustomTokenObtainPairSerializer adds custom claims
        response = self.client.post(
            self.url,
            data={
                'email': 'test@example.com',
                'password': 'testpass123'
            },
            format='json'
        )

        access_token = response.data['access']
        decoded_token = AccessToken(access_token)
        
        # Test for custom claims you've added
        # Example:
        # self.assertEqual(decoded_token['email'], self.user.email)
        # self.assertEqual(decoded_token['custom_claim'], 'expected_value')

    def test_serializer_class(self):
        """Test that the correct serializer class is used"""
        view = CustomTokenObtainPairView()
        self.assertEqual(
            view.serializer_class,
            CustomTokenObtainPairSerializer
        )