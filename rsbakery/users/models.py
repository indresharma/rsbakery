from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.shortcuts import reverse


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required for Registration')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='profiles', default='profiles/default_profile.jpg')
    about_me = models.CharField(max_length=255, blank=True, null=True) 
    location = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)  

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


