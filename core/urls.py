from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('notifications', views.NotificationViewset, basename='notifications')

urlpatterns = [
    path('all-zm/', views.All_ZM_APIViewset.as_view(), name='all_zm'),
    path('all-pm/', views.All_PM_APIViewset.as_view(), name='all_pm'),
    path('all-pc/', views.All_PC_APIViewset.as_view(), name='all_pc'),
    path('all-mis/', views.All_MIS_APIViewset.as_view(), name='all_mis'),
    path('', include(router.urls), name='core_api'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
