"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView

from config.yasg import schema_view

urlpatterns = [
    path('', TemplateView.as_view(template_name='common/home.html')),

    path('admin/', admin.site.urls),
    path('accounts/', include('app_accounts.urls', namespace='accounts')),
    path('telegram/', include('app_telegrambot.urls', namespace='telegram-bot')),
    path('socialauth/', include('app_social_auth.urls', namespace='social-auth')),
    path('api/', include('app_habits.urls', namespace='api')),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + staticfiles_urlpatterns()
