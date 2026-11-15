from django.urls import path
from .views import GoogleLoginView, GitHubLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserProfileView,
    ChangePasswordView,
    LogoutView,
)

urlpatterns = [

    path("register/", UserRegistrationView.as_view(), name="user-register", ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserProfileView.as_view(), name="user-profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("google/", GoogleLoginView.as_view(), name="google-login"),
    path("github/", GitHubLoginView.as_view(), name="github-login"),

]
