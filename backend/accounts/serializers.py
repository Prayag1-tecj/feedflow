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