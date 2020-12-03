from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('centre-excel-logs', views.CentreExcelLogAPIView, basename='centre_excel_logs')
router.register('centre-excel', views.CentreExcelAPIView, basename='centre_excel')
router.register('centres', views.CentreAPIView, basename='centres')
router.register('all-centres', views.AllCentreAPIView, basename='all-centres')

urlpatterns = [
    path('all-zones/', views.All_Zones_APIView.as_view()),
    path('all-city/', views.All_city_APIView.as_view()),
    path('', include(router.urls), name='centre_api'),
]
