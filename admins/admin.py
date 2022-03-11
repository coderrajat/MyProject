from django.contrib import admin

# Register your models here.
from admins import models

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
admin.site.register(models.SubscriptionPlan)
admin.site.register(models.Notification_admin)
admin.site.register(models.Subscription_History)
admin.site.register(models.Generes)
admin.site.register(models.charts_admin)
admin.site.register(models.Feedback)
admin.site.register(models.Points_History)






# admin.site.register(models.CMS)


