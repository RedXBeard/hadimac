# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from hadimac.user.forms import LoginForm, RegistrationForm, EmailOptionsForm
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
                return HttpResponse(u'Bilgiler Yanlış')
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
                           last_name = data['last_name'],
                           get_forum_activity_as_email = data['get_forum_activity_as_email'],
                           get_match_activity_as_email = data['get_match_activity_as_email']).create_key()
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
            mail = EmailMultiAlternatives(u"Hadi Maç Üyelik",
                                          u'Aşağıdaki linke tıklayın.<br><a href="http://%s%s">Tıklayın!</a>'%(domain, reverse('registration-done', args = [key])),
                                          "hadimac@markafoni.com",
                                          [data['email']])
            mail.content_subtype = "html"
            mail.send()
            return HttpResponse(u'Mailinize Bakın.')
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
    up = UserProfile(user = u, get_match_activity_as_email = r.get_match_activity_as_email,
                     get_forum_activity_as_email = r.get_forum_activity_as_email)
    up.save()
    return HttpResponseRedirect(reverse('main', args=[]))

@user_passes_test(lambda u: u.is_superuser)
def create_default_user_profile(request):
    users = auth.models.User.objects.all()
    for user in users:
        try:
            UserProfile.objects.get(user = user)
        except:
            UserProfile.objects.create(user = user, get_forum_activity_as_email = False, get_match_activity_as_email = True)
    return HttpResponseRedirect('/')


@login_required
def email_options(request):
    up = UserProfile.objects.get(user = request.user)
    form = EmailOptionsForm({"get_match_activity_as_email" : up.get_match_activity_as_email,
                             "get_forum_activity_as_email" : up.get_forum_activity_as_email})
    message = ""
    if request.POST:
        form = EmailOptionsForm(request.POST)
        if form.is_valid():
            up.get_match_activity_as_email = form.cleaned_data['get_match_activity_as_email']
            up.get_forum_activity_as_email = form.cleaned_data['get_forum_activity_as_email']
            up.save()
            message = u"Değişiklik Kaydedildi."
    return r("user/email_options.html", {"form" : form, "message" : message}, request)
