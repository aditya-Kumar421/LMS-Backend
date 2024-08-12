from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings

from .serializers import RegisterSerializer, UserSerializer

from datetime import datetime, timedelta
import random
import string

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SendOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = ''.join(random.choices(string.digits, k=6))
            user.otp = otp
            user.save()

            send_mail(
                'Your OTP Code',
                f'Your OTP code is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({"detail": "OTP sent to email."}, status=status.HTTP_200_OK)
        return Response({"detail": "User with this email not found."}, status=status.HTTP_404_NOT_FOUND)


class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # email = request.data.get('email')
        otp = request.data.get('otp')
        user = User.objects.filter(otp=otp).first()
        if user:
            if user.otp == otp:
                user.is_active = True
                user.otp = None 
                user.save()
                return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "User with this email not found."}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        user = User.objects.get(pk=uid)
        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid token or UID."}, status=status.HTTP_400_BAD_REQUEST)


#Currently This functionality Not added 

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}&uid={user.pk}"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response({"detail": "User with this email not found."}, status=status.HTTP_404_NOT_FOUND)

# class VerifyEmailView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, uid, token, *args, **kwargs):
#         user = User.objects.get(pk=uid)
#         token_generator = PasswordResetTokenGenerator()
#         if token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
#         return Response({"detail": "Invalid token or UID."}, status=status.HTTP_400_BAD_REQUEST)
