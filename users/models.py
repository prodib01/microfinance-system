from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from utilities.choices import role_choices


class MuroUserManager(BaseUserManager):
    def create_user(self, email, password, fullname, phone_number, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname,
                          phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, fullname, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, fullname, phone_number, **extra_fields)


class MuroUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MuroUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone_number']

    def __str__(self):
        return self.fullname + ' - ' + self.email


class Profile(models.Model):
    user = models.OneToOneField(MuroUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    role = models.CharField(
        max_length=20, choices=role_choices, default='LOAN_OFFICER')
    branch = models.ForeignKey(
        'branch.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name="user_branch")

    def __str__(self):
        return self.user.fullname