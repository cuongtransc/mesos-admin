from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('list_application')), name='index'),
    url(r'^list-groups$', views.list_groups, name='list_groups'),
    url(r'^new/app-tenant-db$', views.new_apptenantdb, name='new_apptenantdb'),
    url(r'^list/app-tenant-db$', views.list_apptenantdb, name='list_apptenantdb'),
    url(r'^new/application$', views.new_application, name='new_application'),
    url(r'^list/application$', views.list_app, name='list_application'),
    url(r'^action/application/$', views.app_action, name='app_action'),
    url(r'^edit/application/(?P<app_id>\d+)$', views.edit_app, name='edit_app'),
    url(r'^list/domain$', views.list_domain, name='list_domain'),
]
