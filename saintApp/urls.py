from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserGetCreate.as_view(), name='users'),
    path('verify-otp/', views.OTPVerificationView.as_view(), name='otp-verify'),
]