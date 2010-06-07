# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

import datetime, sha, random, time

WEEKDAYS = [u'Pazartesi', u'Salı', u'Çarşamba', u'Perşembe', u'Cuma', u'Cumartesi', u'Pazar']


class Team(models.Model):
    name = models.CharField(max_length = 64)
    color = models.CharField(max_length = 64)
    is_active = models.BooleanField(default = True)

    def __unicode__(self):
        return u"%s"%self.name


class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name = "home")
    away_team = models.ForeignKey(Team, related_name = "away")
    occured_at = models.DateTimeField()
    place = models.CharField(max_length = 512)
    creater = models.ForeignKey(User)
    is_cancelled = models.BooleanField(default = False)
    stack = models.IntegerField()
    is_active = models.BooleanField(default = True)
    formation = models.TextField()
    
    def __unicode__(self):
        return u"%s"%self.occured_at
    
    def humanized_day(self):
        return WEEKDAYS[self.occured_at.weekday()]


class Score(models.Model):
    match = models.ForeignKey(Match)
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __unicode__(self):
        return u"%s-%s:%s-%s"%(self.match.home_team.name, self.match.away_team.name, self.home_score, self.away_score)


class MatchRequest(models.Model):
    home_team = models.ForeignKey(Team, related_name = "requested_home")
    away_team = models.ForeignKey(Team, related_name = "requested_away")
    occured_at = models.DateTimeField()
    place = models.CharField(max_length = 512)
    creater = models.ForeignKey(User)
    stack = models.IntegerField()
    explanation = models.TextField()

    def __unicode__(self):
        return u"%s ? "%self.occured_at

    def humanized_day(self):
        return WEEKDAYS[self.occured_at.weekday()]
      
class MatchSubstitutes(models.Model):
    key        = models.CharField(max_length = 64, null = True, blank = True)
    email      = models.EmailField()
    inviter    = models.ForeignKey(User)
    is_active  = models.BooleanField(default=True) 
    
    def create_key(self):
      x = sha.new("%s%s"%(self.email, random.randint(10000000000000, 99999999999999999)))
      self.key = "%s%s%s"%(x.hexdigest(), random.randint(10000000000000, 99999999999999), ("%s"%(time.time()))[:10])
      self.save()
      return self.key
    def __unicode__(self):
        return u'%s' %self.email
    
