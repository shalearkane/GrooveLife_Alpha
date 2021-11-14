from django.http.response import JsonResponse
from rest_framework import status, viewsets
from rest_framework import filters
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Album, Artist, Genre, History, LikedSong, Track

from .serializers import (
    AlbumSerializer,
    ArtistSerializer,
    GenreSerializer,
    HistorySerializer,
    LikedSongSerializer,
    ListAlbumSerializer,
    ListArtistSerializer,
    ListGenreSerializer,
    SignUpSerializer,
    TrackSerializer,
    UserSerializer,
)

# Create your views here.


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """Just serialize an user, no need to validate"""
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """update user detail"""
        # the request header contains the auth details
        # so the request data contains the json to process

        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class HelloWorldTestView(APIView):
    def post(self, request):
        print(request.data)
        return Response(
            data={"hello": "world", "message": request.data["message"]},
            status=status.HTTP_200_OK,
        )


class TrackView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TrackSerializer
    queryset = Track.objects.all()


class AlbumView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = Album.objects.all()
        serializer = ListAlbumSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Album.objects.all()
        album = get_object_or_404(queryset, pk=pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = Artist.objects.all()
        serializer = ListArtistSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Artist.objects.all()
        artist = get_object_or_404(queryset, pk=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = Genre.objects.all()
        serializer = ListGenreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Genre.objects.all()
        genre = get_object_or_404(queryset, pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikedSongsView(APIView):
    permission_classes = (IsAuthenticated,)

    # post request adds a like song
    def post(self, request):
        request.data["user"] = request.user.id
        serializer = LikedSongSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            likedSong = serializer.save()
            if likedSong:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # put request queries if a liked song exists (get request was not working)
    def put(self, request):
        isLiked = LikedSong.objects.filter(
            user=request.user, track=request.data["track"]
        ).exists()
        return JsonResponse({"isLiked": isLiked})

    # get request gets the list of all liked songs by the user
    def get(self, request):
        queryset = LikedSong.objects.filter(user=request.user).order_by("-time")
        serializer = LikedSongSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete request removes the liked song
    def delete(self, request):
        query = LikedSong.objects.filter(track=request.data["track"], user=request.user)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data["user"] = request.user.id
        serializer = HistorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            listenedSong = serializer.save()
            if listenedSong:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = History.objects.filter(user=request.user).order_by("-time")
        serializer = HistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchTrackView(generics.ListAPIView):
    search_fields = ["track_title", "album__album_title"]
    filter_backends = (filters.SearchFilter,)
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class SearchAlbumView(generics.ListAPIView):
    search_fields = ["album_title"]
    filter_backends = (filters.SearchFilter,)
    queryset = Album.objects.all()
    serializer_class = ListAlbumSerializer


class SearchArtistView(generics.ListAPIView):
    search_fields = ["name"]
    filter_backends = (filters.SearchFilter,)
    queryset = Artist.objects.all()
    serializer_class = ListArtistSerializer
