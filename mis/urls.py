from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('excel_errors', views.ExcelLogAPIView, basename='excel_errors')
router.register('excel', views.ExcelPostAPIView, basename='excel')
router.register('projects', views.ProjectAPIViewset, basename='project')
router.register('project-details', views.ProjectDetailAPIViewset, basename='project-details')

urlpatterns = [
    path('', include(router.urls), name='api'),

    path('allot-zm-zone-wise/', views.AlotZmZoneWise.as_view(), name='allot_zm_zone_wise'),
    path('allot-pc-city-wise/', views.AlotPCCityWise.as_view(), name='allot-pc-city-wise'),

    ## GRAPH URLS ##
    path('count-by-centre-type/', views.CentreTypeCountAPIView.as_view(), name='api'),
    path('count-by-installation-status/', views.InstallationCountAPIView.as_view(), name='api'),
    path('count-by-qc-status/', views.QCStatusCountAPIView.as_view(), name='api'),
    path('count-by-mock-status/', views.MockStatusCountAPIView.as_view(), name='api'),
    path('count-by-disputed-centre/', views.DisputedCentreCountAPIView.as_view(), name='api'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
