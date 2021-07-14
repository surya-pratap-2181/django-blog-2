from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
# Create your models here.

# Model for adding a new blog


class Blog(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    title_slug = models.SlugField(unique=True, default=uuid.uuid1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default='pk')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# From django documentation custom user model creation

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, mobile, auth_token, full_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            mobile=mobile,
            full_name=full_name,
            auth_token=auth_token,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, mobile, auth_token, is_verified, full_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            mobile=mobile,
            full_name=full_name,
            auth_token=auth_token,
        )
        user.is_verified = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=100, default=None)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=14)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'mobile', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
