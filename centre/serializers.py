from rest_framework import serializers
from . import models


class CentreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Centre
        fields = ["id", "zone", "state", "city", "code", "name", "centre_type"]


class AllCentreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Centre
        fields = "__all__"


class CentreExcelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CentreExcel
        fields = "__all__"


class CentreExcelLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CentreExcelLog
        fields = "__all__"

