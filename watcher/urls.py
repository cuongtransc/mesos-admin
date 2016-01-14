from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('list_watcher')), name='index'),
    url(r'^new-watcher$', views.new_watcher, name='new_watcher'),
    url(r'^list-watcher$', views.list_watcher, name='list_watcher'),
    url(r'^ajax-list-watcher$', views.ajax_list_watcher, name='ajax_list_watcher'),
    url(r'^watcher-action$', views.watcher_action, name='watcher_action'),
    url(r'^ajax-notification$', views.ajax_notifications, name='ajax_notifications'),
    url(r'^list-notifications$', views.list_notifications, name='list_notifications'),
    url(r'^ajax-list-notifications$', views.ajax_list_notifications, name='ajax_list_notifications'),
    url(r'^notify-action$', views.notify_action, name='notify_action'),
]
