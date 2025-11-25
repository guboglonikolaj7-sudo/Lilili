from django.urls import path
from .views import RegisterView

app_name = "users"
urlpatterns = [
    path("", RegisterView.as_view(), name="register"),
]
