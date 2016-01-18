from django.conf import settings
from watcher import models
from watcher.utils import *


def start_watcher():
    watchers = models.Watcher.objects.all()
    for watcher in watchers:
        watcher_thread = create_watcher_from_db(watcher.id)
        if watcher.status == '1':
            watcher_thread.start()
    print("Total watcher thread: "+str(len(settings.WATCHER_THREADS)))
