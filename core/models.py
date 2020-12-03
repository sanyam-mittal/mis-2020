from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import UserManager


class PMManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(designation='PM')


class PCManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(designation='PC')


class ZMManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(designation='ZM')


class MISManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(designation='MIS')


class Profile(models.Model):
    designation_choices = (
        ('PM', 'PM'),
        ('ZM', 'ZM'),
        ('PC', 'PC'),
        ('MIS', 'MIS')
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    phone = models.PositiveIntegerField(blank=True, null=True)
    designation = models.CharField(max_length=30, choices=designation_choices, blank=True, null=True)

    objects = models.Manager()
    pm_objects = PMManager()
    zm_objects = ZMManager()
    pc_objects = PCManager()
    mis_objects = MISManager()

    def __str__(self):
        return str(self.user.username)


class Notification(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', blank=True, null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')

    message = models.TextField()
