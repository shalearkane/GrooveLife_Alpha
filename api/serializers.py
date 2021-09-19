from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class SignUpSerializer(serializers.ModelSerializer):
    """This is used to create a new user"""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        else:
            # of course as the password isn't set, so this can't be used to create superuser
            user = User.objects.create_user(**validated_data)
            user.set_password(password)
            user.save()

            return user


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and des of User objects"""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password")

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        # Passwords should not be handled with `setattr`, unlike other fields.
        # Django provides a function that handles hashing and
        # salting passwords. That means
        # we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        
        try:
            password = validated_data.pop("password")
        except KeyError:
            pass
        else :
            if password is not None:
                instance.set_password(password)
        finally : 
            for (key, value) in validated_data.items():
                setattr(instance, key, value)


        instance.save()

        return instance
