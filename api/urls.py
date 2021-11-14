from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from .views import (
    AlbumView,
    ArtistView,
    GenreView,
    SearchAlbumView,
    SearchArtistView,
    SearchTrackView,
    SignUpView,
    HelloWorldTestView,
    TrackView,
    UserRetrieveUpdateView,
    LogoutAndBlacklistRefreshTokenForUserView,
    LikedSongsView,
    HistoryView,
)

router = DefaultRouter()
router.register(r"tracks", TrackView, basename="track")
router.register(r"albums", AlbumView, basename="album")
router.register(r"artists", ArtistView, basename="artist")
router.register(r"genres", GenreView, basename="genre")

urlpatterns = [
    path(
        "token/obtain/", jwt_views.TokenObtainPairView.as_view(), name="token_create"
    ),  # override sjwt stock token
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("user/create/", SignUpView.as_view(), name="create_user"),
    path("user/update/", UserRetrieveUpdateView.as_view(), name="retrive_and_update"),
    path(
        "user/logout/",
        LogoutAndBlacklistRefreshTokenForUserView.as_view(),
        name="logout_and_blacklist_refresh_token",
    ),
    path("likedsongs/", LikedSongsView.as_view(), name="liked_songs"),
    path("history/", HistoryView.as_view(), name="history"),
    path("test/", HelloWorldTestView.as_view(), name="hello_world_test_view"),
    path("search/track/", SearchTrackView.as_view()),
    path("search/albums", SearchAlbumView.as_view()),
    path("search/artist/", SearchArtistView.as_view()),
]

urlpatterns += router.urls
