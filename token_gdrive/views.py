from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import subprocess
from token_gdrive.models import *

# Create your views here.

def index(request):
    return render(request, 'token_gdrive/index.html')

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
