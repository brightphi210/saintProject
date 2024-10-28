from rest_framework import serializers
from .models import *
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        profile = UserProfile.objects.get(user=user)
        token['profile_id'] = profile.id
        token['profile_pic'] = profile.profile_pic
        return token


    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only

    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],  # Add name field to User model
        )


        otp = get_random_string(length=6, allowed_chars='0123456789')
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # Send OTP
        self.send_otp(user.email, otp)
        return user

    def send_otp(self, email, otp):
        send_mail(
            'Welcome to Codex Christi',
            f'Please verify your email with OTP: {otp}',
            'bmpinovations@gmail.com',
            [email],
            fail_silently=False,
        )




class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
        if user.otp_created_at and (timezone.now() - user.otp_created_at).seconds < 60:
            raise serializers.ValidationError("You can only request a new OTP after 1 minute.")
        
        return value

    def resend_otp(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generate a new OTP and update the user model
        otp = get_random_string(length=6, allowed_chars='0123456789')
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # Send OTP via email
        self.send_otp(user.email, otp)

    def send_otp(self, email, otp):
        send_mail(
            'Resend OTP - Codex Christi',
            f'Please verify your email with the new OTP: {otp}',
            'bmpinovations@gmail.com',
            [email],
            fail_silently=False,
        )



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'




class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'], otp=data['otp'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or Email.")

        # Check if OTP has expired (after 10 minutes)
        if timezone.now() > user.otp_created_at + timezone.timedelta(minutes=10):
            raise serializers.ValidationError("OTP has expired.")

        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True  # Activate the user upon successful OTP verification
        user.otp = None  # Clear the OTP
        user.otp_created_at = None  # Clear OTP created time
        user.save()
        return user




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError("New password must be different from the old password.")
        return attrs



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)