from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from marathon import MarathonClient
from django.views.decorators.csrf import csrf_exempt
from marathon_mgmt.utils import *
import json
import html
import traceback
from config_template.models import *

# Create your views here.
@csrf_exempt
def new_app(request):
    data = {}
    if request.method == 'POST':
        data['msg'] = "Post"
        post_params = {}
        for key in request.POST:
            if key.startswith("filehidden"):
                fkey = key[11:]
                if(request.FILES.get(fkey, None)):
                    post_file = request.FILES[fkey]
                    file_content=""
                    for chunk in post_file.chunks():
                        file_content += chunk.decode("utf8")
                    post_params[fkey] = convert(file_content)
                else:
                    post_params[fkey] = request.POST[key]
            else:
                post_params[key] = request.POST[key]


        template = Template.objects.get(pk=post_params['template_id'])
        content = template.content%post_params
        data['content'] = content
        mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
        try:
            mc.create_app_by_json(content)
            data['result'] = "Success"
        except Exception as e:
            data['result'] = str(e)


    templates = Template.objects.filter(type="marathon").all()
    for template in templates:
        template.params = template.param_set.order_by('id')

    data['templates'] = templates
    return render(request, 'marathon_mgmt/new_app.html', data)

def list_app(request):
    mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
    apps = mc.list_apps()
    data = {'apps': apps}
    data['refresh'] = 3000
    return render(request, 'marathon_mgmt/list_app.html', data)


@csrf_exempt
def send_to_marathon(request):
    try:
        if request.method == 'POST':
            action = request.POST.get('action', None)
            app_id = request.POST.get('id', None)
            mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
            if action == 'stop':
                mc.scale_app(app_id, 0)
            elif action == 'start':
                mc.scale_app(app_id, 1)
            elif action == 'destroy':
                mc.delete_app(app_id)
            elif action == 'restart':
                pass
            elif action == 'scale':
                mc.scale_app(app_id, int(request.POST.get('number_instance')))
            result = '{"status":"success", "msg": "%(action)s success"}'%{"action":action}
    except Exception as e:
        result = '{"status":"error", "msg": "%(action)s fail: %(error)s" }'%{"action":action, "error": html.escape(str(e))}
    return HttpResponse(result)

def ajax_list_apps(request):
    mc = MarathonClient('http://{}:{}'.format(settings.MARATHON['host'], settings.MARATHON['port']))
    apps = mc.list_apps()
    data = {'apps': apps}
    return render(request, 'marathon_mgmt/ajax_list_apps.html', data)
