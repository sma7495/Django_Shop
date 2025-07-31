from rest_framework.generics import GenericAPIView
from rest_framework.views import Response, status
from rest_framework.permissions import IsAuthenticated
import jwt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from mail_templated import EmailMessage
from django.contrib.auth import get_user_model

from .serializer import (
    RegistrationSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
)


User = get_user_model()


class RegistrationGenericAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def get_token_for_user(self, user_email):
        user = User.objects.get(email=user_email)
        referesh = RefreshToken.for_user(user)
        return str(referesh.access_token)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user_email = serializer.validated_data["email"]
            token = self.get_token_for_user(user_email)
            from_email = "admin@admin.com"
            host_name = request.get_host()
            message = EmailMessage(
                "emails/account/verify_token.tpl",
                {
                    "token": token,
                    "host_name": host_name,
                },
                from_email,
                to=[user_email],
            )

            message.send()
            return Response(
                {
                    "email": user_email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerifyUserToken(GenericAPIView):
    def get(self, request, token, *args, **kwargs):
        try:
            decode_token = jwt.decode(
                jwt=token, key=api_settings.SIGNING_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "detail": "Token has expired.",
                },
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except jwt.InvalidTokenError:
            return Response(
                {
                    "detail": "Invalid token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = decode_token.get("user_id")
        user = User.objects.get(id=user_id)
        if user.is_active:
            return Response(
                {"detail": "user alrady activated"},
                status=status.HTTP_208_ALREADY_REPORTED,
            )
        else:
            user.is_active = True
            user.save()
            return Response(
                {"detail": "user activated successfully"},
                status=status.HTTP_200_OK,
            )


class UserChangePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serial = self.get_serializer(data=request.data)
        serial.is_valid(raise_exception=True)
        new_pass = serial.validated_data["new_password"]
        self.request.user.set_password(new_pass)
        self.request.user.save()
        return Response(
            {"detail": "Your password changed successfully"},
            status=status.HTTP_200_OK,
        )


class PsswordRecoveryView(GenericAPIView):

    def get(self, request, email, *args, **kwargs):
        try:
            user = User.objects.get(email=email)
        except:
            user =''
            
        from_email = "example@test.com"
        if user:
            if user.is_active:
                random_password = User.objects.make_random_password()
                user.set_password(random_password)
                user.save()
                message = EmailMessage(
                    "emails/account/password_recovery.tpl",
                    {
                        "password": random_password,
                    },
                    from_email,
                    to=[user.email],
                )

                message.send()
                return Response(
                    {"detail": "the new password sent to your email"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "this is not a active user"},
                    status=status.HTTP_400_BAD_REQUEST,
                ) 
        else:
            return Response(
                {"detail": "this is not a vilid user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
