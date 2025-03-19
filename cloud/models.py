from django.db import models

class UploadFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=260, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
