from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        write_only=True
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
            "full_name",
        ]

    def validate_email(self, value):
        if User.objects.filter(
            email=value
        ).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value  

    def create(self, validated_data):
        full_name = validated_data.pop(
            "full_name"
        )

        user = User.objects.create_user(
            **validated_data
        )

        user.profile.full_name = full_name
        user.profile.save()

        return user

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid credentials"
            )

        user = authenticate(
            username=user.username,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials"
            )

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(
                refresh.access_token
            ),
            "refresh": str(refresh),
        }

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="profile.full_name"
    )

    onboarding_completed = serializers.BooleanField(
        source="profile.onboarding_completed"
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "onboarding_completed",
        ]