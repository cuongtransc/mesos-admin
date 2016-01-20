from django.db import models

# Create your models here.
class Group(models.Model):
    id = models.AutoField(primary_key=True)
    instance_id = models.CharField(max_length=200, unique=True)
    instance_ip = models.CharField(max_length=200)
    instance_port = models.CharField(max_length=9)
    class Meta:
        db_table = "nginx_groups"

class AppTenantDB(models.Model):
    id = models.AutoField(primary_key=True)
    host  = models.CharField(max_length=200)
    port  = models.CharField(max_length=200)
    dialect  = models.CharField(max_length=200)
    username  = models.CharField(max_length=200)
    password  = models.CharField(max_length=200)
    db_name  = models.CharField(max_length=200)
    use_tenant = models.CharField(max_length=200)
    app_id = models.CharField(max_length=200)
    class Meta:
        db_table = "nginx_app_tenant_db"

class App(models.Model):
    id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    disabled = models.CharField(max_length=1)
    use_tenant = models.CharField(max_length=200)
    app_id = models.CharField(max_length=200)
    app_tenant_db = models.ForeignKey(AppTenantDB, on_delete=models.CASCADE)
    class Meta:
        db_table = "nginx_apps"
