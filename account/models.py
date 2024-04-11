from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.postgres.fields import ArrayField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class FileUpload(models.Model):
    file = models.FileField(upload_to='account_files')
    def __str__(self):
        return self.file
    
class CustomUser(AbstractUser):
    
    username = models.CharField(primary_key = True, default=1, max_length=135, unique=True)
    email = models.EmailField(max_length=200)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=135)    
    password = models.CharField(max_length=100)
    phone = models.BigIntegerField(default=0)
    date_joined = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ['phone', 'email', 'password']
    email_is_verified = models.BooleanField(default=False)
    object=CustomUserManager()
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class EmailAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='email_addresses')
    email = models.EmailField(max_length=100)  # Adjust the max length as needed
    emailis_verified = models.BooleanField(default=False)

    def _str_(self):
        return self.email



class PhoneNumber(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='phone_numbers')
    phone_number = models.CharField(max_length=25)  
    phoneis_verified = models.BooleanField(default=False)

    def _str_(self):
        return self.phone_number


class UserPhoneNumber(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    is_registered = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    # Additional fields and methods as needed

    def _str_(self):
        return f"{self.username} - {self.phone_number}"

#created another table with foreign key username and email 
class UserEmail(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    is_registered = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    # Additional fields and methods as needed

    def _str_(self):
        return f"{self.username} - {self.email}"
    

class UploadedDocuments(models.Model):
    username = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    newfilename = models.CharField(max_length=100, primary_key=True, unique=True, default=1)
    filename = models.CharField(max_length=200, default=None)
    path = models.URLField(max_length = 500)
    tags = models.CharField(max_length = 200)
    extension = models.CharField(max_length = 10, default="a")
    timenow = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.username
    
