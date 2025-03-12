"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from lost_found_app.views import signup, logout, hello_world, hello_world_api, home, profile, report_lost_item, report_found_item, item_details, dashboard, update_match_status

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('admin/', admin.site.urls),
    path('', include('lost_found_app.urls')),
    path('hello/', hello_world, name='hello_world'),
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('report-lost/', report_lost_item, name='report_lost'),
    path('report-found/', report_found_item, name='report_found'),
    path('item-details/<uuid:id>/', item_details, name='item_details'),
    path('dashboard/', dashboard, name='dashboard'),
    path("update-match-status/", update_match_status, name="update_match_status"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
