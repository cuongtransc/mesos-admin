from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import subprocess
from token_gdrive.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied

# Create your views here.
@login_required
def index(request):
    return render(request, 'token_gdrive/index.html')

@login_required
def add_token(request):
    if request.method == 'GET':
        token = request.GET.get('token', None)
        process = subprocess.Popen(['python2', "{}/gdrive.py".format(settings.DIR_GDRIVE_AUTH), token], cwd=settings.DIR_GDRIVE_AUTH, stdout=subprocess.PIPE)
        out, err = process.communicate()
        credential = Credentials()
        credential.credential = out.decode().split("\n")[1]
        credential.gmail = request.GET.get('gmail', None)
        credential.save()
        return HttpResponse(out.decode().split("\n")[1])
    else:
        return HttpResponse("no sp")
