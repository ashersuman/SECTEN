from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

class AccountUserManager(BaseUserManager):
    def create_user(self, email, aadhaarNo, mobNo, password=None):
        if not email:
            raise ValueError('Please provide a valid email address')
        if not aadhaarNo:
            raise ValueError('Please provide your Aadhaar Number')
        if not mobNo:
            raise ValueError('Please provide a valid Mobile Number')

        user = self.model(
            email = self.normalize_email(email),
            mobNo = mobNo,
            aadhaarNo = aadhaarNo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, aadhaarNo, mobNo, password):
        user = self.create_user(
            email       = self.normalize_email(email),
            aadhaarNo   = aadhaarNo,
            mobNo       = mobNo,
            password    = password,
        )

        user.is_admin = True
        user.is_bidder = False
        user.is_superuser = True

        user.save(using = self._db)
        return user

class AccountUser(AbstractBaseUser):
    mobnovalidator = RegexValidator(r'^[6-9]\d{9}$', 'Enter a valid Mobile Number.')
    aadhaarnovalidator = RegexValidator(r'^[0-9]{12}', 'Enter a valid Aadhaar Number.')

    email       = models.EmailField(max_length=60, unique=True)
    mobNo       = models.CharField(verbose_name="mobile number", max_length=10, unique=True, validators=[mobnovalidator])
    aadhaarNo   = models.CharField(verbose_name="aadhaar number", max_length=12, null=False, unique=True, validators=[aadhaarnovalidator])
    first_name  = models.CharField(verbose_name="first name",max_length=60)
    last_name   = models.CharField(verbose_name="last name", max_length=60)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now=True)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_bidder   = models.BooleanField(default=True)
    is_orgadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['mobNo','aadhaarNo']

    objects = AccountUserManager()

    def __str__(self):
        return self.first_name+" "+self.last_name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
