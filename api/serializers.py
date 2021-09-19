from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class SignUpSerializer(serializers.ModelSerializer):
    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        else:
            # of course as the password isn't set, so this can't be used to create superuser
            user =  User.objects.create_user(**validated_data)
            user.set_password(password)
            user.save()

            return user