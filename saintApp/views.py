from django.shortcuts import render
from . models import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView

# Create your views here.

class UserGetCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserProfileGetView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'


    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)


class OTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User verified successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Set new password
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    


class ResendOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.resend_otp()  # Call the method to resend OTP
            return Response({"detail": "OTP has been resent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
