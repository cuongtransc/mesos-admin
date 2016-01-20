from django.shortcuts import render
from config_template.models import *
from marathon import MarathonClient
from django.conf import settings
import chronos
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
# Create your views here.
@login_required
def dashboard(request):
    data = {}
    data['total_template'] = Template.objects.count()
    mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
    data['total_app'] = len(mc.list_apps())
    cclient = chronos.connect('{}:{}'.format(settings.CHRONOS['host'], settings.CHRONOS['port']))
    jobs = cclient.list()
    data['total_job'] = len(cclient.list())
    data['total_watcher'] = len(settings.WATCHER_THREADS)
    return render(request, 'dashboard/dashboard.html',data)
