from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import User
from user.utils import arrange_permissions
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from user.enums import UserStatusChoices, UserRoleChoices
from user.utils import send_email


class UserBasicSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField("get_role")

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "role")

    def get_role(self, obj):
        return obj.get_role_display()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField("get_role")

    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "status")

    def get_role(self, obj):
        return obj.get_role_display()


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, data):
        credentials = {"username": data.get("username"), "password": data.get("password")}
        user = authenticate(**credentials)
        if user:
            if not user.status == UserStatusChoices.ACTIVE.value:
                raise serializers.ValidationError("Account is not active yet.")
            refresh = self.get_token(user)
            data = {
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
                "user": UserSerializer(user).data,
                "permissions": arrange_permissions(user.get_all_permissions()),
            }
            return data
        else:
            raise serializers.ValidationError("Incorrect/Invalid username or password")


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password", "phone", "birthday", "age", "role")

    def create(self, validated_data):
        role = validated_data.get("role")
        if role == UserRoleChoices.PATIENT.value:
            user = User.objects.create_patient(**validated_data)
        elif role == UserRoleChoices.DOCTOR.value:
            user = User.objects.create_doctor(**validated_data)
        else:
            raise serializers.ValidationError({"invalid": ["Please choose correct role"]})
        send_email(user, validated_data.get("password"))
        return user


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.IntegerField()

    class Meta:
        fields = ("email", "role")


class ResetPasswordSerializer(serializers.Serializer):
    key = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    role = serializers.IntegerField()

    class Meta:
        fields = (
            "key",
            "new_password",
            "confirm_password",
            "role"
        )
        write_only_fields = ("key", "new_password", "confirm_password")

    def validate(self, data):
        encoded_user = data.get("key")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        role = data.get("role")
        token = self.context.get("request").headers.get("Authorization")
        if not token:
            raise serializers.ValidationError("Token is required")
        decoded_user = urlsafe_base64_decode(encoded_user).decode()
        user = User.objects.get(email=decoded_user, role=role)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is expired or invalid")
        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New password and confirm password must match"
            )
        user.set_password(new_password)
        user.save()
        return data


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    role = serializers.IntegerField()

    class Meta:
        fields = (
            "old_password",
            "new_password",
            "confirm_password",
            "role"
        )
        write_only_fields = ("old_password", "new_password", "confirm_password")

    def validate(self, data):
        request = self.context.get("request")
        email = request.user.email
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        role = data.get("role")
        user = User.objects.get(email=email, role=role)
        if not check_password(old_password, user.password):
            raise serializers.ValidationError("old password is incorrect")
        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New password and confirm password must match"
            )
        user.set_password(new_password)
        user.status = UserStatusChoices.ACTIVE.value
        user.save()
        return data
