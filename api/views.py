from os import access
from rest_framework import serializers, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Album, Track

from .serializers import (
    AlbumSerializer,
    ListAlbumSerializer,
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
