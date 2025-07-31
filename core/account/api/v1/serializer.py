from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

# from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ...models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "password doesnt match!"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1")
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user_id"] = self.user.id
        data["user_email"] = self.user.email

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=256)
    new_password = serializers.CharField(max_length=256)
    new_password1 = serializers.CharField(max_length=256)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "password doesnt match!"})

        if not self.context.get("request").user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"detail": "old password is incorect!"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return super().validate(attrs)
