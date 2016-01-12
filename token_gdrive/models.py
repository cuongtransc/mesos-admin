from django.db import models

# Create your models here.
class Credentials(models.Model):
    gmail = models.CharField(max_length=200)
    credential = models.TextField()
    class Meta:
        db_table = "credentials"
