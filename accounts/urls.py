from django.urls import path
from .views import UserDetailView, UserListView, register_view, UserUpdateView, UserDeleteView, UserPasswordChangeView, \
    password_reset_email_view, PasswordResetFormView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'
urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/add/', register_view, name='user_add'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_edit'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/password_change/', UserPasswordChangeView.as_view(), name='user_password_change'),
    path('reset-password/', password_reset_email_view, name='password_reset_email'),
    path('reset-password/<token>/', PasswordResetFormView.as_view(), name='password_reset_form')

]