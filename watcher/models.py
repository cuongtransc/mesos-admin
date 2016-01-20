from django.db import models

# Create your models here.
class Watcher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=1, default='0')
    config = models.TextField(default='')
    created_at = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "watchers"
        permissions = (
            ("can_destroy", "Can destroy watcher"),
            ("can_run", "Can start, stop, restart watcher"),
        )

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    watcher = models.ForeignKey(Watcher, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "notifications"
