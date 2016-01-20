from django.db import models
from django.contrib.auth.models import Permission

class PermMarathon(Permission):
    class Meta:
        proxy = True
        permissions = (
            ("can_init_app", "Can add new, delete app"),
            ("can_run_app", "Can start, stop, restart, scale app"),
        )
