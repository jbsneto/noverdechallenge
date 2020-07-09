"""noverdechallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='', # TODO: por o título aqui
        default_version='v1',
        contact=openapi.Contact(email=""),  # TODO: por o email aqui
    ),
    public=True,
)

urlpatterns = [
    path('', schema_view.with_ui('redoc'), name='schema-redoc'), # Doc
    # TODO: No doc deles pede o /load sem nada na frente
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger<format>', schema_view.without_ui(), name='schema-json'), # Doc
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]
