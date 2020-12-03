from rest_framework import serializers
from . import models


class ExcelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Excel
        fields = "__all__"


class ExcelLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ExcelLog
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = "__all__"


class ProjectDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectDetail
        fields = "__all__"
