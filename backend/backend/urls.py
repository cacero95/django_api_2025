from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('api/v1/', include('example.urls')),
    path('api/v1/', include('categories.urls')),
    path('api/v1/', include('recipe.urls')),
    path('api/v1/', include('contact.urls')),
    path('api/v1/', include('security.urls')),
    path('api/v1/', include('recipes_helpers.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)