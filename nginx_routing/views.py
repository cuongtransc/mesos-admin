from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from nginx_routing.models import *
import html
import json

# Create your views here.
def list_tenants(request):
    tenants = Tenant.objects.all()
    groups = Group.objects.all()
    data = {}
    data['tenants'] = tenants
    data['groups'] = groups
    return render(request, 'nginx_routing/list_tenants.html', data)

def list_groups(request):
    groups = Group.objects.all()
    data = {}
    data['groups'] = groups
    return render(request, 'nginx_routing/list_groups.html', data)

def group_action(request):
    groups = Group.objects.all()
    data = {}
    data['groups'] = groups
    return render(request, 'nginx_routing/list_groups.html', data)

#################################################################
def list_apptenantdb(request):
    apptenantdbs = AppTenantDB.objects.all()
    data = {}
    data['apptenantdbs'] = apptenantdbs
    return render(request, 'nginx_routing/list_apptenantdbs.html', data)

@csrf_exempt
def new_apptenantdb(request):
    data = {}
    if request.method == 'POST':
        try:
            apptdb = AppTenantDB()
            apptdb.host = request.POST.get("host")
            apptdb.port = request.POST.get("port")
            apptdb.dialect = request.POST.get("dialect")
            apptdb.username = request.POST.get("username")
            apptdb.password = request.POST.get("password")
            apptdb.db_name = request.POST.get("db_name")
            apptdb.save()
            result = '{"status": "success", "msg": "Add app-tenant-db success"}'
            return HttpResponse(result)
        except Exception as e:
            result = '{"status": "error", "msg": "Error: %s "}'% str(e).replace("\n", " ").replace('"', '\\"')
            return HttpResponse(result)

    else:
        return render(request, 'nginx_routing/new_apptenantdb.html', data)
###################################################################
@csrf_exempt
def new_application(request):
    data = {}
    if request.method == 'POST':
        try:
            app = App()
            app.domain_name = request.POST.get("domain_name")
            app.disabled = request.POST.get("disabled")
            app.use_tenant = request.POST.get("use_tenant")
            app.marathon_app_id = request.POST.get("marathon_app_id")
            if (request.POST.get("use_tenant")=='1'):
                apptdb = AppTenantDB()
                apptdb.host = request.POST.get("host")
                apptdb.port = request.POST.get("port")
                apptdb.dialect = request.POST.get("dialect")
                apptdb.username = request.POST.get("username")
                apptdb.password = request.POST.get("password")
                apptdb.db_name = request.POST.get("db_name")
                apptdb.save()
                app.app_tenant_db = apptdb
            else:
                app.app_tenant_db = None
            app.save()
            result = '{"status": "success", "msg": "Add app-tenant-db success"}'
            return HttpResponse(result)
        except Exception as e:
            result = '{"status": "error", "msg": "Error: %s "}'% str(e).replace("\n", " ").replace('"', '\\"')
            return HttpResponse(result)

    else:
        return render(request, 'nginx_routing/new_application.html', data)

def list_app(request):
    apps = App.objects.all()
    data = {}
    data['apps'] = apps
    return render(request, 'nginx_routing/list_app.html', data)

@csrf_exempt
def app_action(request):
    try:
        if request.method == 'POST':
            action = request.POST.get('action', None)
            if action == 'delete':
                app_id = request.POST.get('id')
                app = App.objects.get(pk=app_id)
                app.delete()
            elif action == 'start':
                pass

            result = '{"status":"success", "msg": "%(action)s success"}'%{"action":action}
    except Exception as e:
        result = '{"status":"error", "msg": "%(action)s fail: %(error)s" }'%{"action":action, "error": str(e).replace("\n", " ").replace('"', '\\"')}
    return HttpResponse(result)

@csrf_exempt
def edit_app(request, app_id):
    app = App.objects.get(pk=app_id)
    if request.method == 'POST':
        try:
            app.domain_name = request.POST.get("domain_name")
            app.disabled = request.POST.get("disabled")
            app.use_tenant = request.POST.get("use_tenant")
            app.marathon_app_id = request.POST.get("marathon_app_id")
            if (request.POST.get("use_tenant")=='1'):
                apptdb = app.app_tenant_db
                if apptdb == None:
                    apptdb = AppTenantDB()
                apptdb.host = request.POST.get("host")
                apptdb.port = request.POST.get("port")
                apptdb.dialect = request.POST.get("dialect")
                apptdb.username = request.POST.get("username")
                apptdb.password = request.POST.get("password")
                apptdb.db_name = request.POST.get("db_name")
                apptdb.save()
                app.app_tenant_db = apptdb
            else:
                if app.app_tenant_db != None:
                    temp  = app.app_tenant_db
                    app.app_tenant_db = None
                    temp.delete()
            app.save()
            result = '{"status": "success", "msg": "Edit app-tenant-db success"}'
            return HttpResponse(result)
        except Exception as e:
            result = '{"status": "error", "msg": "Error: %s "}'% str(e).replace("\n", " ").replace('"', '\\"')
            return HttpResponse(result)
    data = {"app": app}
    return render(request, 'nginx_routing/edit_application.html', data)
