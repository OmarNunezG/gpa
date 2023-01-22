from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    # path("/", views.user_view, name="user"),
    path("register/", views.register, name="register"),
    path("auth/", views.auth, name="auth"),
]
