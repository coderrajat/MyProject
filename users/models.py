from django.db import models
from accounts.models import Users
from admins.models import songs
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your models here.


class Recommended_Songs_by_admin(models.Model):
    user=models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='recommended_songs',null=True,blank=True)    
    songs=models.ManyToManyField(songs,blank=True,null=True, related_name='recommended_to_user')

class Notification_user(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE,null=True,blank=True,related_name="user_notify")
    status=models.CharField(max_length=264,null=True,blank=True,default="unread")
    type_of_notification=models.CharField(max_length=264,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def save(self, *args, **kwargs):
        from .serializers import Notification_data
        print("Notification was saved")
        channel_layer = get_channel_layer()
        notifications_unread = Notification_user.objects.filter(status = "unread").count()
        notifications = Notification_user.objects.all().order_by('created_at')[:9]
        data = {
            'notifications_unread': notifications_unread + 1,
            'notifications': Notification_data(notifications, many=True).data,
            #'notifications': serializers.serialize('json', notifications),
            'current_notification': Notification_data(self).data
            #'current_notification': serializers.serialize('json', [self])
        }

        async_to_sync(channel_layer.group_send)(
            'admin_group', {
                'type': 'send_notification',
                'value': json.dumps(data)
            }   
        )

        super(Notification_user, self).save(*args, **kwargs)

