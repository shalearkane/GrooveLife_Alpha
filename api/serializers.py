from django.db.models import fields
from .models import History, LikedSong, User, Track, Album, Genre, Artist
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
        else:
            if password is not None:
                instance.set_password(password)
        finally:
            for (key, value) in validated_data.items():
                setattr(instance, key, value)

        instance.save()
        return instance


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        depth = 2
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    track = TrackSerializer(many=True)

    class Meta:
        model = Album
        depth = 1
        fields = ("artist", "genre", "album_title", "album_logo", "track")


class ListAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        depth = 1
        fields = "__all__"


class ArtistSerializer(serializers.ModelSerializer):
    album_artist = ListAlbumSerializer(many=True)

    class Meta:
        model = Artist
        depth = 1
        fields = ("name", "thumbnail", "bio", "country", "album_artist")


class ListArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        depth = 1
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    album_genre = ListAlbumSerializer(many=True)

    class Meta:
        model = Genre
        depth = 1
        fields = ("name", "album_genre")


class ListGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        depth = 1
        fields = "__all__"


# PrimaryKeyRelatedField may be used to represent the target of the relationship using its primary key.


class LikedSongSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all(), many=False)

    class Meta:
        model = LikedSong
        fields = "__all__"

    def to_representation(self, instance):
        print(super().to_representation(instance))
        response = super().to_representation(instance)
        response["track"] = TrackSerializer(instance.track).data
        return response


class HistorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all(), many=False)

    class Meta:
        model = History
        fields = "__all__"

    def to_representation(self, instance):
        print(super().to_representation(instance))
        response = super().to_representation(instance)
        response["track"] = TrackSerializer(instance.track).data
        return response
