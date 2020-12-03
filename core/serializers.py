from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = models.Profile
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notification
        fields = "__all__"
