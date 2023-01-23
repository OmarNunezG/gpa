from django.urls import path
from transaction import views

app_name = "transaction"

urlpatterns = [
    path("transfer/", views.transfer, name="transfer"),
]
