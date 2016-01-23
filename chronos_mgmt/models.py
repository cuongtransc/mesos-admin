from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.
class PermChronos(Permission):
    class Meta:
        proxy = True
        permissions = (
            ("can_init_job", "Can create, delete job"),
            ("can_run_job", "Can start, stop, job"),
        )
