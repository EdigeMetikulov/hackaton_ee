from django.db import models
from django.contrib.auth.hashers import make_password  # hash
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save

# from apps.account.services.signals import post_create_cart_signal


class CustomUserManager(UserManager):

    def _create_user(self, email, password, username=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        is_user = extra_fields.pop("is_user")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        if is_user:
            user.generate_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username=None, **extra_fields):  # обычный пользователь
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields["is_user"] = True
        return self._create_user(email, password, username=None, **extra_fields)

    def create_superuser(self, email, password=None, username=None, **extra_fields):  # superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields["is_active"] = True
        extra_fields["is_user"] = False

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, username=None, **extra_fields)


    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj):
        return self.is_staff


class CustomUser(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=150)
    is_active = models.BooleanField(default=False)
    activate_code = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", ]

    objects = CustomUserManager()

    def generate_code(self):
        self.activate_code = self.generate_activation_code(16, "12345qwerty")

    @staticmethod
    def generate_activation_code(length: int, number_range: str):
        from django.utils.crypto import get_random_string
        return get_random_string(length, number_range)


# post_save.connect(post_create_cart_signal, CustomUser)
