from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str

from hadimac.mac.models import Match, Team

import datetime, sha, random, time


class UserFault(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User)
    match = models.ForeignKey(Match)

    @staticmethod
    def is_user_has_fault(user):
        return user.userfault_set.filter(owner = user).count() > 0

    
class Attendance(models.Model):
    attendee = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    team = models.ForeignKey(Team, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    is_cancelled = models.BooleanField(default = False)

    def __unicode__(self):
        return smart_str(self.attendee.get_full_name())

    @staticmethod
    def is_user_attended(user, match):
        return Attendance.objects.filter(attendee = user, match = match, is_cancelled = False).count() > 0


class Register(models.Model):
    key = models.CharField(max_length = 64, null = True, blank = True)
    email = models.EmailField()
    passwd = models.CharField(max_length = 30)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def create_key(self):
        x = sha.new("%s%s"%(self.email, random.randint(10000000000000, 99999999999999999)))
        self.key = "%s%s%s"%(x.hexdigest(), random.randint(10000000000000, 99999999999999), ("%s"%(time.time()))[:10])
        self.save()
        return self.key
