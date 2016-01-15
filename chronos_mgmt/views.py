from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import html
import traceback
from config_template.models import *
import chronos
import dateutil.parser


# Create your views here.
@csrf_exempt
def new_job(request):
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
        cclient = chronos.connect('{}:{}'.format(settings.CHRONOS['host'], settings.CHRONOS['port']))
        try:
            print(type(json.loads(content)))
            cclient.add(json.loads(content))
            data['result'] = "Success"
        except Exception as e:
            data['result'] = str(e)


    templates = Template.objects.filter(type="chronos").all()
    for template in templates:
        template.params = template.param_set.order_by('id')

    data['templates'] = templates
    return render(request, 'chronos_mgmt/new_job.html', data)

def list_job(request):
    cclient = chronos.connect('{}:{}'.format(settings.CHRONOS['host'], settings.CHRONOS['port']))
    jobs = cclient.list()
    for job in jobs:
        last_success = job['lastSuccess']
        last_error = job['lastError']

        if last_success == "" and last_error != "":
            job['last'] = "error"
        elif last_success != "" and last_error == "":
            job['last'] = "success"
        elif last_success != "" and last_error != "":
            last_success = dateutil.parser.parse(job['lastSuccess'])
            last_error = dateutil.parser.parse(job['lastError'])
            if last_error > last_success:
                job['last'] = "error"
            else:
                job['last'] = "success"
        elif last_success == "" and last_error == "":
            job['last'] = "-"

        job['stat'] = cclient.job_stat(job['name'])['histogram']
    data = {'jobs': jobs}
    data['refresh'] = 3000
    return render(request, 'chronos_mgmt/list_job.html', data)


@csrf_exempt
def send_to_chronos(request):
    try:
        if request.method == 'POST':
            action = request.POST.get('action', None)
            job_name = request.POST.get('name', None)
            cclient = chronos.connect('{}:{}'.format(settings.CHRONOS['host'], settings.CHRONOS['port']))
            if action == 'destroy':
                cclient.delete(job_name)
            elif action == 'run':
                cclient.run(job_name)

            result = '{"status":"success", "msg": "%(action)s success"}'%{"action":action}
    except Exception as e:
        result = '{"status":"error", "msg": "%(action)s fail: %(error)s" }'%{"action":action, "error": html.escape(str(e))}
    return HttpResponse(result)

def ajax_list_job(request):
    cclient = chronos.connect('{}:{}'.format(settings.CHRONOS['host'], settings.CHRONOS['port']))
    jobs = cclient.list()
    for job in jobs:
        last_success = job['lastSuccess']
        last_error = job['lastError']

        if last_success == "" and last_error != "":
            job['last'] = "error"
        elif last_success != "" and last_error == "":
            job['last'] = "success"
        elif last_success != "" and last_error != "":
            last_success = dateutil.parser.parse(job['lastSuccess'])
            last_error = dateutil.parser.parse(job['lastError'])
            if last_error > last_success:
                job['last'] = "error"
            else:
                job['last'] = "success"
        elif last_success == "" and last_error == "":
            job['last'] = "-"

        job['stat'] = cclient.job_stat(job['name'])['histogram']
    data = {'jobs': jobs}
    return render(request, 'chronos_mgmt/ajax_list_job.html', data)
