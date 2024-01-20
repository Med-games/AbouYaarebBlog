from django.contrib import admin
from .models import Post,Comment,video
from embed_video.admin import AdminVideoMixin

class AdminVideo(AdminVideoMixin,admin.ModelAdmin):
    pass
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(video,AdminVideo)
