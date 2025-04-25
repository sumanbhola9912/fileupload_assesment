from django.contrib import admin
from .models import FileUpload

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'file', 'status', 'timestamp', 'note')
    list_filter = ('status',)
    search_fields = ('user_email', 'file')
