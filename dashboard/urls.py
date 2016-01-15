from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
]
