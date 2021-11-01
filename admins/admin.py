from django.contrib import admin

# Register your models here.
from admins import models
from .models import artist,album,songs
# Register your models here.
admin.site.register(models.CMS)
admin.site.register(models.faq)
admin.site.register(models.social_media_settings)
admin.site.register(models.image_settings)
admin.site.register(models.general_settings)
admin.site.register(models.SMTP_setting)
admin.site.register(models.artist)
admin.site.register(models.album)
admin.site.register(models.songs)
admin.site.register(models.playlist_admin)



# admin.site.register(models.CMS)


