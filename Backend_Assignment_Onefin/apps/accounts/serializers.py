from .models import AuthUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator, EmailValidator


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[
        validate_password,
        RegexValidator(
            regex='^(?=.*[a-z])(?=.*[A-Z]).{8,}$',
            message='Password must be at least 8 characters long and contain at least one uppercase and one lowercase letter.'
        )
    ])

    class Meta:
        model = AuthUser
        fields = '__all__'
