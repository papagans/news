from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserDetailView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'
urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]