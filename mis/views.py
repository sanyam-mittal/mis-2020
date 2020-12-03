from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response
from rest_framework import permissions, generics, viewsets, authentication
from rest_framework.views import APIView
from . import serializers, tasks
from mis import models
from centre import models as centre_models


class ExcelPostAPIView(viewsets.ModelViewSet):
    queryset = models.Excel.objects.all()
    serializer_class = serializers.ExcelSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.AllowAny,)

    # def get_queryset(self):
    #     if self.action == 'list':
    #         queryset = models.Excel.objects.filter(errors=0)
    #     else:
    #         queryset = models.Excel.objects.all()
    #     return queryset


class ExcelLogAPIView(viewsets.ModelViewSet):
    queryset = models.ExcelLog.objects.all()
    serializer_class = serializers.ExcelLogSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self, pk=None):
        excel_id = self.request.query_params.get('excel' or None)
        if pk:
            log = models.ExcelLog.objects.get(id=pk)
        elif excel_id:
            log = models.ExcelLog.objects.filter(excel_file__id=excel_id)
        else:
            log = models.ExcelLog.objects.all()
        return log

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProjectAPIViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        queryset = models.Project.av_objects.all()
        get_user_projects = self.request.query_params.get('user' or None)

        if get_user_projects and user.is_authenticated:
            designation = user.profile.designation
            if designation == 'PM':
                queryset = queryset.filter(zm=None)
            elif designation == 'ZM':
                queryset = queryset.filter(zm__id=user.id, pc=None)
            elif designation == 'PC':
                queryset = queryset.filter(pc__id=user.id, zm=None)
        return queryset

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProjectDetailAPIViewset(viewsets.ModelViewSet):
    queryset = models.ProjectDetail.objects.all()
    serializer_class = serializers.ProjectDetailSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


################ ALOT ZM AND PC ##################

class AlotZmZoneWise(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        zone = request.data['zone']
        zm = request.data['zm']
        zm_user = User.objects.get(id=zm)
        projects = None
        count = 0
        for i in zone:
            projects = models.Project.av_objects.filter(centre__zone__icontains=i, zm=None)
            projects.update(zm=zm_user)
            count += projects.count()
        if len(zone)>0:
            return Response(count)
        else:
            return Response(count)


class AlotPCCityWise(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        city = request.data['city']
        pc = request.data['pc']
        pc_user = User.objects.get(id=pc)
        projects = None
        count = 0
        for i in city:
            projects = models.Project.av_objects.filter(centre__city__icontains=i, pc=None)
            projects.update(pc=pc_user)
            count += projects.count()
        if len(city) > 0:
            return Response(count)
        else:
            return Response(count)


####################### GRAPH VIEWS ##################


class CentreTypeCountAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        centre_types = models.ProjectDetail.centre_type_choices
        result = {}
        data = []
        chart = {
            "caption": "Centres of different types",
            "subCaption": "",
            "xAxisName": "Centre Types",
            "yAxisName": "Count",
            "numberSuffix": "",
            "theme": "fusion"
        }
        for i in centre_types:
            values = {'label': i[1],
                      'value': models.ProjectDetail.objects.filter(centre_type__icontains=str(i[0])).count()}
            data.append(values)

        result["data"] = data
        result["chart"] = chart
        return Response(result)


class InstallationCountAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        types = models.ProjectDetail.installation_status_choices
        result = {}
        data = []
        chart = {
            "caption": "Installation status of Centres",
            "subCaption": "",
            "xAxisName": "Installation Status",
            "yAxisName": "Count",
            "numberSuffix": "",
            "theme": "fusion"
        }
        for i in types:
            values = {'label': i[1],
                      'value': models.ProjectDetail.objects.filter(installation_status__icontains=str(i[0])).count()}
            data.append(values)

        result["data"] = data
        result["chart"] = chart
        return Response(result)


class QCStatusCountAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        types = models.ProjectDetail.qc_status_choices
        result = {}
        data = []
        chart = {
            "caption": "Different QC status of Centres",
            "subCaption": "",
            "xAxisName": "QC Status",
            "yAxisName": "Count",
            "numberSuffix": "",
            "theme": "fusion"
        }
        for i in types:
            values = {'label': i[1],
                      'value': models.ProjectDetail.objects.filter(qc_status__icontains=str(i[0])).count()}
            data.append(values)

        result["data"] = data
        result["chart"] = chart
        return Response(result)


class MockStatusCountAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        types = models.ProjectDetail.mock_status_choices
        result = {}
        data = []
        chart = {
            "caption": "Different Mock status of Centres",
            "subCaption": "",
            "xAxisName": "Mock Status",
            "yAxisName": "Count",
            "numberSuffix": "",
            "theme": "fusion"
        }
        for i in types:
            values = {'label': i[1],
                      'value': models.ProjectDetail.objects.filter(mock_status__icontains=str(i[0])).count()}
            data.append(values)

        result["data"] = data
        result["chart"] = chart
        return Response(result)


class DisputedCentreCountAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        types = [("disputed", True), ("non_disputed", False)]
        result = {}
        data = []
        chart = {
            "caption": "Disputed centres",
            "subCaption": "",
            "xAxisName": "Centres",
            "yAxisName": "Count",
            "numberSuffix": "",
            "theme": "fusion"
        }
        for i in types:
            values = {'label': i[0],
                      'value': models.ProjectDetail.objects.filter(disputed_centre=i[1]).count()}
            data.append(values)

        result["data"] = data
        result["chart"] = chart
        return Response(result)
