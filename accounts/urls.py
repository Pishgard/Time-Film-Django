from django.urls import path
from . import views
from rest_framework_simplejwt import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),

    path('token/refresh/', auth_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('request-reset-phone/', views.RequestPasswordResetPhone.as_view(), name='request-reset-phone'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]