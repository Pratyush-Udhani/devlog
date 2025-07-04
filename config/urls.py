"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from logs.views import (
    LogEntryCreateView,
    LogEntryDeleteView,
    IndexView,
    LogEntryFormView,
    LogEntryUnifiedView
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from logs.views_api import (
    LogEntryAPICreateView,
    LogEntryAPIListView
)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('admin/', admin.site.urls, name='admin'),

    path("logs/", LogEntryUnifiedView.as_view(), name="get_logs"),
    path('logs/create/', LogEntryCreateView.as_view(), name='create_log'),
    path('logs/<int:pk>/delete/', LogEntryDeleteView.as_view(), name="delete_log"),
    path("logs/new/", LogEntryFormView.as_view(), name="create_log_form"),

    # CLI/POSTMAN API routes
    path("api/logs/", LogEntryAPIListView.as_view(), name="api_list_logs"),
    path("api/logs/create/", LogEntryAPICreateView.as_view(), name="api_create_log"),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
