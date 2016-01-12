from django.conf.urls import url
from . import views
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('list_template')), name='index'),
    url(r'^new-template$', views.new_template, name='new_template'),
    url(r'^list-template$', views.list_template, name='list_template'),
    url(r'^edit-template/(?P<template_id>\d+)$', views.edit_template, name='edit_template'),
    url(r'^delete-template/(?P<template_id>\d+)$', views.delete_template, name='delete_template'),
    url(r'^ajax-new-template$', views.ajax_new_template, name='ajax_new_template'),
    url(r'^ajax-edit-template$', views.ajax_edit_template, name='ajax_edit_template'),
]
