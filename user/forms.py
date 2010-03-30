# -*- coding: utf-8 -*-

from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User

from hadimac.user.models import Register

class LoginForm(forms.Form):
    email = forms.EmailField(label = u'Email', max_length = 256)
    password = forms.CharField(label = u"Parola", required = True, widget = forms.PasswordInput())

class RegistrationForm(forms.Form):
    email = forms.EmailField(label = u'Email', max_length = 256)
    password1 = forms.CharField(label = u"Parola", required = True, widget = forms.PasswordInput())
    password2 = forms.CharField(label = u"Parola Tekrar", required = True, widget = forms.PasswordInput())
    first_name = forms.CharField(label = u"Ad", max_length = 30)
    last_name = forms.CharField(label = u"Soyad", max_length = 30)
    get_forum_activity_as_email = forms.BooleanField(label = u"Forumda yazılanları email adresime yolla")
    get_match_activity_as_email = forms.BooleanField(label = u"Her yeni maç bilgisini email adresime yolla", initial = True)

    def validate(self):
        data = self.cleaned_data
        is_correct = True
        
        if data['password1'] != data['password2']:
            self.errors['password2'] = ErrorList([u'Bu şifre bir önceki ile aynı olmalıdır!'])
            is_correct = False

        if User.objects.filter(email = data['email']).count():
            self.errors['email'] = ErrorList([u'Daha önce kaydolmuşsunuz.'])
            is_correct = False

        if Register.objects.filter(is_active = True, email = data['email']):
            self.errors['email'] = ErrorList([u"Bu email ile kayıt isteği zaten var. akin.kok@akinon.com'a mail atarak durumu cözebilirsiniz."])

#         mail_domain = data['email'].split('@')[1].split('.')
#         if not mail_domain == 'markafoni' and not mail_domain == 'akinon':
#             self.errors['email'] = ErrorList([u'Akinon yada Markafoni Mailleri Kabul Gormekte..'])
#             is_correct = False

        return is_correct

class EmailOptionsForm(forms.Form):
    get_forum_activity_as_email = forms.BooleanField(label = u"Forumda yazılanları email adresime yolla", required = False)
    get_match_activity_as_email = forms.BooleanField(label = u"Her yeni maç bilgisini email adresime yolla", required = False)
