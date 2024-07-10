from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import (UserRegisterView, UserDetailView, UserUpdateView, GeneratePasswordView, email_verification,
                         UserListView, block_user)

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', UserRegisterView.as_view(), name='register'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('email.confirm/<str:verification_code>/', email_verification, name='email_verification'),
    path('reset_pass', GeneratePasswordView.as_view(template_name='users/reset_password.html'), name='reset_pass'),

    path('list/', UserListView.as_view(), name='list_users'),
    path('block_user/<int:pk>', block_user, name='block_user')
]
