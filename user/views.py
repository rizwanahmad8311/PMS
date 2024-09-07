from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import User
from user.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
    UpdatePasswordSerializer,
)
from rest_framework import generics, status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.communication import (
    send_mail_using_smtp,
    get_mail_template,
)
from django.conf import settings
from user.swagger import get_token_swagger
from user.enums import UserStatusChoices


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()


class UserLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class ForgetPasswordView(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        front_end_url = request.headers.get("Origin")
        settings.FRONT_END_URL = front_end_url
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.get(email=email)
        if not user.status == UserStatusChoices.ACTIVE.value:
            return Response(
                {
                    "message": "failure",
                    "errors": [
                        "You cannot reset your password as your account is not active"
                    ],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        encoded_user = urlsafe_base64_encode(force_bytes(user.email))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = (
            f"{settings.FRONT_END_URL}/auth/signin?key={encoded_user}&token={token}"
        )
        email_data = {
            "from": settings.EMAIL_HOST_USER,
            "subject": "Password Reset Link",
            "message": get_mail_template("reset", {"reset_link": reset_link}),
            "recipient": [email],
        }
        send_mail_using_smtp(email_data)
        return Response(
            {"data": f"Reset password link has been sent to you on {email}"},
            status=status.HTTP_200_OK,
        )

@get_token_swagger()
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"data": "Password reset successfully"}, status=status.HTTP_200_OK
        )


class UpdatePasswordView(generics.GenericAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response({"data": "Password Updated successfully"})
