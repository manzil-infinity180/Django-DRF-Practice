from django.db import models

# Create your models here.
class Demo(models.Model):
    user = models.ForeignKey('auth.User',related_name='demo',null=True,on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=150)
    code = models.TextField(blank=True)
    linenos = models.BooleanField(default=False)
    language =  models.CharField(max_length=100, default='python')
    style = models.CharField(max_length=100, default='friendly')