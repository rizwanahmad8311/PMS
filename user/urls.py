from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user import views

app_name = "user"
urlpatterns = [
    # Auth urls
    path("register/", views.UserRegistrationView.as_view(), name="register-user"),
    path("login/", views.UserLoginView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "forget-password/", views.ForgetPasswordView.as_view(), name="forget-password"
    ),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path(
        "update-password/", views.UpdatePasswordView.as_view(), name="update-password"
    ),
]
