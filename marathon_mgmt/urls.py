from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('list_app')), name='index'),
    url(r'^list-app$', views.list_app, name='list_app'),
    url(r'^new/(?P<type>\w+)$', views.new_app, name='new_app'),
    url(r'^send-to-marathon$', views.send_to_marathon, name='send_to_marathon'),
    url(r'^ajax-list-apps$', views.ajax_list_apps, name='ajax_list_apps'),
]
