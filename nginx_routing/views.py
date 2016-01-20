from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from nginx_routing.models import *

# Create your views here.
def list_tenants(request):
    tenants = Tenant.objects.all()
    groups = Group.objects.all()
    data = {}
    data['tenants'] = tenants
    data['groups'] = groups
    return render(request, 'nginx_routing/list_tenants.html', data)
