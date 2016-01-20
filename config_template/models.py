from django.db import models

# Create your models here.
class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    content = models.TextField()
    type = models.CharField(max_length=20, default='marathon')
    class Meta:
        db_table = "templates"

class Param(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    default = models.TextField(max_length=200)
    class Meta:
        db_table = "params"
