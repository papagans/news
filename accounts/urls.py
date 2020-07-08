from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserDetailView

app_name = 'accounts'
urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]