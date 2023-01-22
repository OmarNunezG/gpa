from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path("create/", views.create_account, name="create"),
]
