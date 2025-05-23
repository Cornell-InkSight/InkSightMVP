"""
URL configuration for InkSightMVP project.

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
from django.urls import path, include
from .run_migrations import run_migrations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('coursemanagement/', include('coursemanagement.urls')),
    path('schoolmanagement/', include('schoolmanagement.urls')),
    path('lecturesessionsmanagement/', include('lecturesessionsmanagement.urls')),
    path('notepacketsmanagement/', include('notepacketsmanagement.urls')),
    path('notetakingrequestmanagement/', include('notetakingrequestmanagement.urls')),
    path('permissionsmanagement/', include('permissionsmanagement.urls')),
    path('usermanagement/', include('usermanagement.urls')),
    path('aimodelmanagement/', include('aimodelmanagement.urls')),
    path("run-migrations/", run_migrations, name="run_migrations"),
]


