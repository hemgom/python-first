from django.db import models

class ViewerHistory(models.Model):
    file_name = models.CharField(max_length=260, null=False)
    file_size = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
