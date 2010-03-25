from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from hadimac.user.forms import LoginForm, RegistrationForm
from hadimac.shortcuts import r
from hadimac.user.models import *

import datetime, sha, random, time

def hadimac_login(request):
    if request.POST:
        form = LoginForm(data = request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                auth.logout(request)
            # give session to the logged in user
            user = auth.authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password"])
            if user is not None:
                auth.login(request, user)
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                else:
                    return HttpResponseRedirect(reverse("main", args=[]))
            else:
                return HttpResponse('Bilgiler Yanlis')
        else:
            # form is invalid so user is still anonymous, give the invalid form back to the user
            request.session.set_test_cookie()
            return r('user/login.html', {'form': form}, request)
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('main')
        form = LoginForm()
        return r('user/login.html', {'form' : form}, request)

def hadimac_logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect(reverse('hadimac-login'))

def register_step1(request):
    form = RegistrationForm()
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid() and form.validate():
            data = form.cleaned_data
            key = Register(email = data['email'],
                           passwd = data['password1'],
                           first_name = data['first_name'],
                           last_name = data['last_name']).create_key()
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
            mail = EmailMultiAlternatives("Hadi Mac Uyelik",
                                          'Asagidaki linke tiklayin.<br><a href="http://%s%s">Tiklayin!</a>'%(domain, reverse('registration-done', args = [key])),
                                          "hadimac@markafoni.com",
                                          [data['email']])
            mail.content_subtype = "html"
            mail.send()
            return HttpResponse('Mailinize Bakin.')
    return r("user/registration.html", {'form' : form}, request)


def register_step2(request, key):
    r = get_object_or_404(Register, key = key)
    if not r.is_active:
        raise Http404
    r.is_active = False
    r.save()
    x = sha.new('%s%s%s'%(r.email, random.randint(100000000, 1000000000000), ('%s'%time.time())[:10]))
    user_name = x.hexdigest()[:30]
    u = auth.models.User(email = r.email, username = user_name, first_name = r.first_name, last_name = r.last_name)
    u.set_password(r.passwd)
    u.save()
    return HttpResponseRedirect(reverse('main', args=[]))
    
