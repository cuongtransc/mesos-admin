"""mesos_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import patterns, include, url
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from mesos_admin import startup
urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard:dashboard')), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^token-gdrive/', include('token_gdrive.urls', namespace="token_gdrive")),
    url(r'^marathon/', include('marathon_mgmt.urls', namespace="marathon_mgmt")),
    url(r'^chronos/', include('chronos_mgmt.urls', namespace="chronos_mgmt")),
    url(r'^config-template/', include('config_template.urls', namespace="config_template")),
    url(r'^watcher/', include('watcher.urls', namespace="watcher")),
    url(r'^dashboard/', include('dashboard.urls', namespace="dashboard")),
]

startup.start_watcher()
