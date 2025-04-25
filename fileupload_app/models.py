from django.db import models
from django.contrib.auth.models import User

class FileUpload(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user_email = models.EmailField()
    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user_email} - {self.file.name}'
