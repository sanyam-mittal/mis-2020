from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/login/', core_views.CustomAuthToken.as_view(), name='rest-login'),
    path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/core/', include('core.urls')),
    path('api/mis/', include('mis.urls')),
    path('api/centre/', include('centre.urls')),
]
