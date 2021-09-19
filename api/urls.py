from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import SignUpView, HelloWorldTestView, UserRetrieveUpdateView

urlpatterns = [
    path(
        "token/obtain/", jwt_views.TokenObtainPairView.as_view(), name="token_create"
    ),  # override sjwt stock token
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("user/create/", SignUpView.as_view(), name="create_user"),
    path("user/update/", UserRetrieveUpdateView.as_view(), name="retrive_and_update"),
    path("test/", HelloWorldTestView.as_view(), name="hello_world_test_view"),
]
