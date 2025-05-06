from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# swagger imports
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Django + React',
        default_version='v1',
        description='Api for Recipes with django',
        terms_of_service='https://www.linkedin.com/in/carlos-andres-acero-sanchez-609224182/',
        contact=openapi.Contact(email='cacero@gmail.com'),
        license=openapi.License(name='BSD License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('api/v1/', include('example.urls')),
    path('api/v1/', include('categories.urls')),
    path('api/v1/', include('recipe.urls')),
    path('api/v1/', include('contact.urls')),
    path('api/v1/', include('security.urls')),
    path('api/v1/', include('recipes_helpers.urls')),
    path('docs<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='shema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='shema-redoc')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)