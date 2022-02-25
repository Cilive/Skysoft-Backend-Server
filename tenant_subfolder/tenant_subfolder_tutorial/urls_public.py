from django.conf.urls import include
from django.urls import path
from django.contrib import admin


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

from .views import CompanyTokenObtainPairView
from rest_framework_simplejwt.views import (
 
    TokenRefreshView,
)



schema_view = get_schema_view(
    openapi.Info(
        title="Skysoft API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # path('', HomeView.as_view()),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('administrator/',include('administrator.urls')),
    path('login/',CompanyTokenObtainPairView.as_view(),name='login'),    
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

