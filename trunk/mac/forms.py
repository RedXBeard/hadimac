from django import forms
from django.forms.util import ErrorList

from hadimac.mac.models import *


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

        return is_correct

class MatchTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset = Team.objects.all())
