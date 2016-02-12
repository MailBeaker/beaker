
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from base.models import RandomIDModel
from base.models import RandomIntIDModel


class MBUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a MBUser with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MBUser(AbstractBaseUser, RandomIntIDModel):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MBUserManager()

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email address already exists.",
        }
    )
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_platform = models.BooleanField(default=False)
    is_webapp = models.BooleanField(default=True)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class EmailMeta(RandomIDModel):
    domain = models.ForeignKey('beaker.Domain')
    email = models.CharField(max_length=512)
    billed = models.BooleanField(default=False)
    thumbnail_url = models.CharField(max_length=512, default=None, blank=True, null=True)
    history_id = models.BigIntegerField(default=0)
    whitelisted = models.BooleanField(default=False)
    blacklisted = models.BooleanField(default=False)
    display_name = models.CharField(max_length=512, default='')


class UserMeta(RandomIDModel):
    user = models.OneToOneField('MBUser')
    organization = models.ForeignKey('beaker.Organization', default=None, blank=True, null=True)
    email_meta = models.ForeignKey('authentication.EmailMeta', default=None, blank=True, null=True)

    @classmethod
    def get_by_user(cls, user):
        try:
            return cls.objects.all().filter(user=user).get()
        except TypeError:
            return None
        except UserMeta.DoesNotExist:
            return None

    @classmethod
    def create_user_meta(cls, user, **kwargs):
        user_meta = cls(user=user, **kwargs)
        user_meta.save()
        return user_meta

    @classmethod
    def get_or_create_user_meta(cls, user, **kwargs):
        um = cls.get_by_user(user)
        if not um:
            um = cls.create_user_meta(user, **kwargs)
        return um

    @classmethod
    def get_by_username(cls, username):
        try:
            user = User.objects.get(username__exact=username)
        except TypeError:
            return None
        except User.DoesNotExist:
            return None

        return cls.get_by_user(user)
