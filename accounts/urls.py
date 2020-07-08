from django.urls import path
from .views import UserDetailView, UserListView, register_view, UserUpdateView, UserDeleteView
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

]