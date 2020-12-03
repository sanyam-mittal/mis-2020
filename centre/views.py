from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response
from rest_framework import permissions, viewsets, authentication
from rest_framework.views import APIView
from . import serializers, tasks
from . import models


class CentreAPIView(viewsets.ModelViewSet):
    queryset = models.Centre.objects.filter(removed=False)
    serializer_class = serializers.CentreSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.AllowAny,)


class AllCentreAPIView(viewsets.ModelViewSet):
    queryset = models.Centre.objects.filter(removed=False)
    serializer_class = serializers.AllCentreSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.AllowAny,)


class CentreExcelAPIView(viewsets.ModelViewSet):
    queryset = models.CentreExcel.objects.all()
    serializer_class = serializers.CentreExcelSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.AllowAny,)


class CentreExcelLogAPIView(viewsets.ModelViewSet):
    queryset = models.CentreExcelLog.objects.all()
    serializer_class = serializers.CentreExcelLogSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self, pk=None):
        excel_id = self.request.query_params.get('excel' or None)
        if pk:
            log = models.CentreExcelLog.objects.get(id=pk)
        elif excel_id:
            log = models.CentreExcelLog.objects.filter(excel_file__id=excel_id)
        else:
            log = models.CentreExcelLog.objects.all()
        return log

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


#################################################
class All_Zones_APIView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        zones = models.Centre.av_objects.values_list('zone', flat=True)
        zones = set(zones)

        return Response(zones)


class All_city_APIView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        values = models.Centre.av_objects.values_list('city', flat=True)
        values = set(values)

        return Response(values)
