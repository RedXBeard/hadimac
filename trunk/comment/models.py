from django.db import models

from django.contrib.auth.models import User
from django.utils.encoding import smart_str

from hadimac.mac.models import *


class Comment(models.Model):
    match = models.ForeignKey(Match)
    user = models.ForeignKey(User)
    title = models.CharField(max_length = 128)
    content = models.CharField(max_length = 512)
    created_at = models.DateTimeField(auto_now_add = True)
    is_visible = models.BooleanField(default = True)
    
    def __unicode__(self):
        return smart_str(self.user.get_full_name()) + " " + smart_str(self.title)
