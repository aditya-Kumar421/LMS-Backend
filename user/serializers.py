from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'fullname','role', 'profile_pic', 'is_active', 'is_staff')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'fullname','password', 'role', 'profile_pic')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            fullname=validated_data['fullname'],
            role=validated_data['role'],
            profile_pic=validated_data.get('profile_pic', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user