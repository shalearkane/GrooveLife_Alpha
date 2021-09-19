from os import access
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer, UserSerializer

# Create your views here.

class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request) :
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
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            RefreshToken(token=refresh_token).blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            


class HelloWorldTestView(APIView):

    def post(self, request):
        print(request.data)
        return Response(data={"hello":"world", "message" : request.data["message"]}, status=status.HTTP_200_OK)