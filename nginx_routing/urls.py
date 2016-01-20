from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('list_tenants')), name='index'),
    url(r'^list-tenants$', views.list_tenants, name='list_tenants'),

]
