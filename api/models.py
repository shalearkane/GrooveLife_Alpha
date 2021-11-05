from enum import unique
from django.conf import settings
from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.deletion import CASCADE, DO_NOTHING, SET

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username.split()[0]


class Artist(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(
        upload_to="artist", default=settings.MEDIA_ROOT + "/artist/default.png"
    )
    bio = models.TextField(verbose_name="Artist Bio", null=True, blank=True)
    country = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Album(models.Model):
    artist = models.ForeignKey(Artist, related_name="album_artist", on_delete=SET(1))
    genre = models.ForeignKey(Genre, related_name="album_genre", on_delete=SET(1))
    album_title = models.CharField(max_length=500)
    album_logo = models.FileField(
        upload_to="album", default=settings.MEDIA_ROOT + "/album_art/default.png"
    )

    def __str__(self) -> str:
        return self.album_title + " - " + self.artist.name


class Track(models.Model):
    album = models.ForeignKey(Album, related_name="track", on_delete=SET(1))
    track_title = models.CharField(max_length=250)
    audio_file = models.FileField(
        upload_to="track", default=settings.MEDIA_ROOT + "/track/track.mp3"
    )

    def __str__(self) -> str:
        return self.track_title


class LikedSong(models.Model):
    user = models.ForeignKey(User, related_name="user_like", on_delete=CASCADE)
    track = models.ForeignKey(Track, related_name="liked_track", on_delete=CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "track")

    def __str__(self) -> str:
        return self.user.username + " - " + self.track.track_title


class History(models.Model):
    user = models.ForeignKey(User, related_name="user_listened", on_delete=CASCADE)
    track = models.ForeignKey(Track, related_name="listened_track", on_delete=CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username + " - " + self.track.track_title
