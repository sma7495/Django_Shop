from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.settings import api_settings
import jwt


from ...api.v1.views import RegistrationGenericAPIView  # Update with your actual import path

User = get_user_model()


class RegistrationGenericAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "password1": "securepassword123",
            # Add other required fields from your RegistrationSerializer
        }
        self.invalid_data = {
            "email": "notanemail",
            "password": "short",
            "password1": "notmatching",
        }
        self.url = "/accounts/api/v1/registration/"  # Update with your actual URL

    def test_get_token_for_user(self):
        # Setup
        user = User.objects.create_user(
            email="test_for_get_token_@example.com",
            password="testpass123",
        )
        view = RegistrationGenericAPIView()

        # Test
        token = view.get_token_for_user(user.email)

        # Verify by reconstructing what should have been generated
        expected_token = str(RefreshToken.for_user(user).access_token)
        
        # Instead of comparing the strings, compare the decoded versions
        decoded_actual = jwt.decode(
                jwt=token, key=api_settings.SIGNING_KEY, algorithms=["HS256"]
            )
        decoded_expected = jwt.decode(
                jwt=expected_token, key=api_settings.SIGNING_KEY, algorithms=["HS256"]
            )
        self.assertEqual(decoded_actual['user_id'], user.id)  # This is the default claim
        self.assertIsNotNone(decoded_actual['exp'])  # expiration exists
        self.assertIsNotNone(decoded_actual['iat'])  

        self.assertEqual(decoded_expected['user_id'], user.id)  # This is the default claim
        self.assertIsNotNone(decoded_expected['exp'])  # expiration exists
        self.assertIsNotNone(decoded_expected['iat'])  
    # Add other claims you expect in the token

    def test_successful_registration(self):
        # Test
        response = self.client.post(
            self.url,
            data=self.valid_data,
            format="json",
        )
        print(response.data)
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], self.valid_data["email"])

        # Verify user was created
        self.assertTrue(User.objects.filter(email=self.valid_data["email"]).exists())

        # Verify email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.valid_data["email"]])
        self.assertEqual(email.from_email, "admin@admin.com")

    def test_registration_with_invalid_data(self):
        # Test
        response = self.client.post(
            self.url,
            data=self.invalid_data,
            format="json",
        )

        # Verify
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertIn("email", response.data)  # assuming email validation error
        #self.assertIn("password", response.data)  # assuming password validation error
        self.assertFalse(User.objects.filter(email=self.invalid_data["email"]).exists())
        self.assertEqual(len(mail.outbox), 0)  # no email sent for invalid data

    def test_registration_with_existing_email(self):
        # Setup - create user with same email first
        User.objects.create_user(
            email=self.valid_data["email"],
            password="existingpass123",
        )

        # Test
        response = self.client.post(
            self.url,
            data=self.valid_data,
            format="json",
        )

        # Verify
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)  # assuming email uniqueness validation
        self.assertEqual(len(mail.outbox), 0)  # no email sent for duplicate registration

    def test_email_template_variables(self):
        # Test
        host = "testserver"
        response = self.client.post(
            self.url,
            data=self.valid_data,
            format="json",
            HTTP_HOST=host,
        )

        # Verify
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        
        # For template testing, you might need to use Django's test Client instead of APIClient
        # or mock the email sending to inspect the template context