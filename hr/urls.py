"""hr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from leave import views as leave_views

urlpatterns = [

    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_URL,
    }),
    url(r'^admin/', admin.site.urls),
    url(r'^logout$', leave_views.logout_view, name='staff_logout'),
    url(r'^dashboard/$', leave_views.dashboard, name='dashboard'),
    url(r'^$', leave_views.login_view, name='staff_login')

] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
