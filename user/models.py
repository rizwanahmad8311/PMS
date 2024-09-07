from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from user import enums
from utils.utils import get_enum_choices
from django.contrib.auth.models import Permission


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_patient(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 3)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 1)
        return self._create_user(username, email, password, **extra_fields)

    def create_doctor(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 2)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    role = models.PositiveIntegerField(choices=get_enum_choices(enums.UserRoleChoices))
    status = models.CharField(
        choices=get_enum_choices(enums.UserStatusChoices),
        default=enums.UserStatusChoices.PENDING.value,
        max_length=10,
    )
    phone = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(
        max_length=6,
        choices=get_enum_choices(enums.UserGenderChoices),
        blank=True,
        null=True,
    )
    birthday = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def get_role(self):
        return self.get_role_display()

    def __str__(self):
        return f"{self.email} | {self.role} | {self.status}"


class ModulePermission(models.Model):
    module = models.CharField(max_length=100)
    permission = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.module

    class Meta:
        db_table = "module_permission"
