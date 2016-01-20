from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.
class PermChronos(Permission):
    class Meta:
        proxy = True
        permissions = (
            ("chronos_can_destroy", "Can destroy job"),
            ("chronos_can_run", "Can start, stop, restart job"),
        )
