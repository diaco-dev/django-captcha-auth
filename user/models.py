from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
from django.db import models
# User = get_user_model()

# class CustomUser(AbstractUser):
#     # username = None
#     email = models.EmailField(unique=True)
#
#     mobile = models.CharField(max_length=15, )
#     is_active = models.BooleanField(default=False)
#     role = models.CharField(max_length=50, default="user", choices=[("user", "User"), ("super_user", "Super User")])
#     username = None  # Remove the default username field
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.email
# from django.contrib.auth.models import AbstractUser
# from django.db import models

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        # if not email:
        #     raise ValueError('The Email field must be set')
        # email = self.normalize_email(email)
        # user = self.model(email=email, **extra_fields)
        # user.set_password(password)
        # user.is_staff = True
        # user.is_superuser = True
        # user.save(using=self._db)
        # return user
        if not email:
            raise ValueError('The Email field must be set')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('role') != 'superuser':
            raise ValueError('Superuser must have role="superuser".')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# class CustomUser(AbstractUser):
#     username = None  # حذف فیلد username
#     email = models.EmailField(unique=True)  # استفاده از ایمیل به عنوان شناسه منحصربه‌فرد
#     mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
#
#     USERNAME_FIELD = 'email'  # ایمیل به عنوان شناسه اصلی برای ورود
#     REQUIRED_FIELDS = ['first_name', 'last_name']  # فیلدهای ضروری هنگام ایجاد کاربر
#
#     objects = CustomUserManager()  # اضافه کردن مدیر سفارشی
#
#     def str(self):
#         return self.email
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superuser', 'Superuser'),
        ('operator', 'Operator'),
        ('user', 'User'),
    ]
    username = None
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    # role = models.CharField(
    #     max_length=10,
    #     choices=[
    #         ('superuser', 'Superuser'),
    #         ('operator', 'Operator'),
    #         ('user', 'User'),
    #     ],
    #     default='user'
    # )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# class CustomUserManager(models.Manager):
#     def create_user(self, email, password=None, **extra_fields):
#         """
#         ایجاد یک کاربر عادی با ایمیل به جای username
#         """
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.is_active = True
#         user.save(using=self._db)
#         return user