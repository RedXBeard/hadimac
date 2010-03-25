from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label = u'Email', max_length = 256)
    password = forms.CharField(label = u"Parola", required = True, widget = forms.PasswordInput())

class RegistrationForm(forms.Form):
    email = forms.EmailField(label = u'Email', max_length = 256)
    password1 = forms.CharField(label = u"Parola", required = True, widget = forms.PasswordInput())
    password2 = forms.CharField(label = u"Parola Tekrar", required = True, widget = forms.PasswordInput())
    first_name = forms.CharField(label = u"Isim", max_length = 30)
    last_name = forms.CharField(label = u"Soy Isim", max_length = 30)

    def validate(self):
        data = self.cleaned_data
        is_correct = True
        
        if data['password1'] != data['password2']:
            self.errors['password2'] = ErrorList([u'Bu sifre bir onceki ile ayni olmali!'])
            is_correct = False

        if User.objects.filter(email = data['email']).count():
            self.errors['email'] = ErrorList([u'Daha once kaydolmussunuz.'])
            is_correct = False

#         mail_domain = data['email'].split('@')[1].split('.')
#         if not mail_domain == 'markafoni' and not mail_domain == 'akinon':
#             self.errors['email'] = ErrorList([u'Akinon yada Markafoni Mailleri Kabul Gormekte..'])
#             is_correct = False

        return is_correct
