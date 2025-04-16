from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import AdminPost


@admin.register(AdminPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'image_tag']

    list_display_links = ['title']

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "no image"

    image_tag.short_description = 'Image Preview'
