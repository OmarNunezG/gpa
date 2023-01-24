from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from user import views

app_name = "user"

urlpatterns = [
    path("accounts/", views.user_accounts, name="user-accounts"),
    path("register/", views.register, name="register"),
    path(
        "token/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
