from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path("create/", views.create_account, name="create"),
    path(
        "balance/<str:account_number>/",
        views.get_balance,
        name="get_balance",
    ),
    path(
        "<str:account_number>/transactions/",
        views.account_transactions,
        name="account_transactions",
    ),
]
