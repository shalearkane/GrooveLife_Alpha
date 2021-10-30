from django.contrib import admin
from .models import Album, Artist, Genre, Track, User, LikedSong, History

# Register your models here.
class CustomUser(admin.ModelAdmin):
    model = User


admin.site.register(User, CustomUser)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(LikedSong)
admin.site.register(History)
