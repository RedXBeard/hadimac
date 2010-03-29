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
            self.errors['away_team'] = ErrorList([u'Home ile Away Ayni Olamaz.'])

        if Match.objects.filter(occured_at = data['occured_at']):
            is_correct = False
            self.errors['occured_at'] = ErrorList([u'Bu anda baska bir mac var.'])

        if data['occured_at'] < datetime.datetime.now():
            is_correct = False
            self.errors['occured_at'] = ErrorList([u'Mac gecmiste kaldi ise millete ne.'])

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
    occured_at = mdoels.DateTimeField(help_text = "")
    home_team = forms.ModelChoiceField(queryset = Team.objects.all(), "Ev Sahibi Takim")
    away_team = forms.ModelChoiceField(queryset = Team.objects.all(), "Misafir Takin")
