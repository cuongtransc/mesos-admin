from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('list_job')), name='index'),
    url(r'^list-job$', views.list_job, name='list_job'),
    url(r'^new-job$', views.new_job, name='new_job'),
    url(r'^send-to-chronos$', views.send_to_chronos, name='send_to_chronos'),
    url(r'^ajax-list-job$', views.ajax_list_job, name='ajax_list_job'),
]
