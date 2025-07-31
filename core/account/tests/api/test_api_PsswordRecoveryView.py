from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ...api.v1.views import PsswordRecoveryView  # Update import path

User = get_user_model()


class PasswordRecoveryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@example123.com',
            password='originalpassword',
            is_active=True
        )
        self.non_existent_email = 'nonexistent@example.com'
        self.url = '/accounts/api/v1/password_recovery/'  # Update with your actual URL

    def test_successful_password_recovery(self):
        """Test password recovery for existing user"""
        response = self.client.get(
            f'{self.url}{self.user.email}/'  # Note the trailing slash
        )

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['detail'],
            'the new password sent to your email'
        )

        # Verify user's password was changed
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('originalpassword'))

        # Verify email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.user.email])
        self.assertEqual(email.from_email, "example@test.com")

        # Verify new password
        new_password = email.body[19:] #extracting new e,ail from email body
        self.assertTrue(self.user.check_password(new_password))

    def test_nonexistent_user(self):
        """Test password recovery for non-existent user"""
        response = self.client.get(
            f'{self.url}{self.non_existent_email}/'
        )

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            'this is not a vilid user'
        )

        # Verify no email was sent
        self.assertEqual(len(mail.outbox), 0)

    def test_inactive_user(self):
        """Test password recovery for inactive user"""
        inactive_user = User.objects.create_user(
            email='inactive@example.com',
            password='originalpassword',
            is_active=False
        )

        response = self.client.get(
            f'{self.url}{inactive_user.email}/'
        )

        # Verify response - adjust based on your desired behavior
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            'this is not a active user'
        )

    def test_email_content(self):
        """Test the email template contains the password"""
        # This requires mocking or testing the template separately
        # Here's a basic version:
        from django.template.loader import render_to_string
        
        test_password = "testpass123"
        email_content = render_to_string(
            "emails/account/password_recovery.tpl",
            {"password": test_password}
        )
        
        self.assertIn(test_password, email_content)