from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new-token$', views.index, name='index'),
    url(r'^add-token$', views.add_token, name='add_token'),
    url(r'^list-token$', views.list_token, name='list_token'),
    url(r'^credential-action$', views.credential_action, name='credential_action'),
]
