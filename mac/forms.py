# -*- coding: utf-8 -*-

from django import forms
from django.forms.util import ErrorList

from hadimac.mac.models import *

import datetime

class MatchForm(forms.Form):
    place = forms.CharField(max_length = 512, label = u"Mekan")
    occured_at = forms.DateTimeField(label = u"Zaman", widget = forms.DateTimeInput, help_text = '12/22/2010 10:00:00')
    stack = forms.IntegerField()
    home_team = forms.ModelChoiceField(queryset = Team.objects.all())
    away_team = forms.ModelChoiceField(queryset = Team.objects.all())
    
    def validate(self):
        data = self.cleaned_data
        is_correct = True

        if data['home_team'].id == data['away_team'].id:
            is_correct = False
            self.errors['away_team'] = ErrorList([u'Home ile Away aynı olamaz.'])

        if Match.objects.filter(occured_at = data['occured_at']):
            is_correct = False
            self.errors['occured_at'] = ErrorList([u'Bu anda başka bir maç var.'])

        if data['occured_at'] < datetime.datetime.now():
            is_correct = False
            self.errors['occured_at'] = ErrorList([u'Maç geçmişte kaldı ise millete ne.'])

        return is_correct

class MatchTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset = Team.objects.all())


class MatchRequest(models.Model):
    home_team = models.ForeignKey(Team, related_name = "requested_home")
    away_team = models.ForeignKey(Team, related_name = "requested_away")
    occured_at = models.DateTimeField()
    place = models.CharField(max_length = 512)
    creater = models.ForeignKey(User)
    stack = models.IntegerField()
    explanation = models.TextField()


class MatchRequestForm(forms.Form):
    occured_at = forms.DateTimeField(label = u"Zaman", widget = forms.DateTimeInput, help_text = "12/22/2010 10:00:00")
    home_team = forms.ModelChoiceField(queryset = Team.objects.all(), label = "Ev Sahibi Takım")
    away_team = forms.ModelChoiceField(queryset = Team.objects.all(), label = "Misafir Takım")
    place = forms.CharField(max_length = 512, label = "Maç Nerede Oynanacak?")
    stack = forms.IntegerField(label = "Kaç Kişilik?")
    explanation = forms.CharField(widget = forms.widgets.Textarea, label = "Kısa bir açıklama yazın.")

    def validate(self):
        data = self.cleaned_data
        is_correct = True

        if data['home_team'].id == data['away_team'].id:
            is_correct = False
            self.errors['away_team'] = ErrorList([u'Home ile Away aynı olamaz.'])

        if MatchRequest.objects.filter(occured_at = data['occured_at']) or Match.objects.filter(occured_at = data['occured_at']) :
            is_correct = False
            self.errors['occured_at'] = ErrorList([u'Bu anda başka bir maç ya da istek var.'])

        if data['occured_at'] < datetime.datetime.now():
            is_correct = False
            self.errors['occured_at'] = ErrorList([u'Maç gecmişte kaldı ise millete ne.'])

        return is_correct
