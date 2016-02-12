
import binascii
import os
from random import randint

from django.db import models


def pkgen():
    """
    Returns a random 24 character string to use as a primary key for a database model.
    """
    return binascii.b2a_hex(os.urandom(12))


def intpkgen():
    """
    Returns a random 16 digit integer to use as a primary key for a database model.

    This is used for MBUser, which is required to have an integer primary key.

    We limit it to 16 digits because of INTEGER field size limitations.
    """
    return randint(10 ** 15, (10 ** (16) - 1))


class RandomIDModel(models.Model):
    id = models.CharField(primary_key=True, max_length=24, default=pkgen)

    class Meta:
        abstract = True

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.objects.get(id=_id)
        except cls.DoesNotExist:
            return None


class RandomIntIDModel(models.Model):
    id = models.BigIntegerField(primary_key=True, default=intpkgen)

    class Meta:
        abstract = True

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.objects.get(id=_id)
        except cls.DoesNotExist:
            return None
