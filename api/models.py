from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.deletion import DO_NOTHING, SET

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username.split()[0]

class Artist(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="artist", default="settings.MEDIA_ROOT/default.png")
    bio = models.TextField(verbose_name='Artist Bio', null=True, blank=True)
    country = models.CharField(max_length=255, blank = True)
    def __str__(self):
        return self.name

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=SET('Anonymous'))
    album_title = models.CharField(max_length=500)
    album_logo = models.FileField(upload_to="album" , default="settings.MEDIA_ROOT/default.png")
    def __str__(self):
        return self.album_title + ' - ' + self.artist.name

class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=SET('Independent Track'))
    track_title = models.CharField(max_length=250)
    audio_file = models.FileField(upload_to="track" , default="settings.MEDIA_ROOT/default.png")
    
    def __str__(self):
        return self.song_title