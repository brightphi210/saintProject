from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserGetCreate.as_view(), name='users'),
    path('user-profile/', views.UserProfileGetView.as_view(), name='user-profile'),
    path('user-profile/update/<str:pk>/', views.UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('verify-otp/', views.OTPVerificationView.as_view(), name='otp-verify'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend-otp'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]