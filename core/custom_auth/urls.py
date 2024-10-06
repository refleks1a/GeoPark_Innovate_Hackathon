from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (CustomUserLoginView, CustomUserCreationView, LogoutView, CustomUserProfileView,
                    verify_email, verify_email_success, verify_email_confirm, verify_email_complete, change_password)


app_name = 'custom_auth'

urlpatterns = [
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('signup/', CustomUserCreationView.as_view(), name='signup'),
    path('logout/', LogoutView, name='logout'),

    path('change_password/', change_password, name='change_password'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(), name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/', CustomUserProfileView.as_view(), name='profile'),

    path('verify_email/', verify_email, name='verify_email'),
    path('verify_email/success/', verify_email_success, name='verify_email_success'),
    path('verify_email_confirm/<uidb64>/<token>/', verify_email_confirm, name='verify_email_confirm'),
    path('verify_email/complete/', verify_email_complete, name='verify_email_complete'),
]
