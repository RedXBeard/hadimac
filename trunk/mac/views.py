# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from hadimac.mac.models import Match
from hadimac.comment.models import Comment
from hadimac.shortcuts import r
from hadimac.mac.forms import MatchForm, MatchTeamForm, Team
from hadimac.user.models import Attendance, UserFault

import datetime

@login_required
def active_matches(request):
    now = datetime.datetime.now()
    lst = list(Match.objects.all().order_by('-occured_at'))
    for m in lst:
        m.is_attended = Attendance.is_user_attended(request.user, m)
        m.number_of_att = m.attendance_set.filter(is_cancelled = False).count()
        m.is_old = m.occured_at < now
    form = MatchTeamForm()
    return r('user/match_list.html', {'list' : lst, 'form' : form}, request)

@login_required
def attendees(request, match_id):
    match = get_object_or_404(Match, id = match_id)
    comments = Comment.objects.filter(match = match, is_visible = True)
    home_players = match.home_team.attendance_set.filter(is_cancelled = False, match = match)
    away_players = match.away_team.attendance_set.filter(is_cancelled = False, match = match)
    return r('user/attendees.html', {'match' : match,
                                      'home_players' : home_players,
                                      'away_players' : away_players,
                                      'comments' : comments,
                                      'score' : match.score_set.all()}, request)

@login_required
def attend(request, match_id):
    if request.POST:
        match = get_object_or_404(Match, id = match_id)

        team = get_object_or_404(Team, id = request.POST.get('team', None))
        if not team: 
            raise Http404

        now = datetime.datetime.now()
        if match.occured_at < now -  settings.MIN_TIME_TO_CANCELATION or\
                UserFault.objects.filter(owner = request.user, match__occured_at__gte = now - datetime.timedelta(days = 7)):
            raise Http404

        if  match.attendance_set.filter(is_cancelled = False).count() >= match.stack:
            return HttpResponse(u'Aktivite Dolu!')

        if team.attendance_set.filter(match = match).count() >= (match.stack / 2):
            return HttpResponse(u'Takım Dolu!')

        if not Attendance.is_user_attended(request.user, match):
            obj, is_created = Attendance.objects.get_or_create(attendee = request.user, match = match)
            obj.is_cancelled = False
            obj.team = team
            obj.save()
        return HttpResponseRedirect(reverse('active-match-list'))

    else:
        return HttpResponse(u'Takim Seçin!')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_match(request):
    form = MatchForm()
    if request.POST:
        form = MatchForm(request.POST)
        if form.is_valid() and form.validate():
            data = form.cleaned_data
            occured_at = data['occured_at']
            match = Match.objects.create(occured_at = occured_at,
                                         place = data['place'],
                                         creater = request.user,
                                         stack = data['stack'],
                                         home_team = data['home_team'],
                                         away_team = data['away_team'])
            subject = u"%s tarihinde oynanacak maç sistemde açıldı." % match.occured_at.date().__str__()
            body = u"Oynamak isteyenler lütfen sistemden kayıt olunuz. \n\n http://hadimac.test.akinon.com" 
            from_email = "hadimac@akinon.com"
            users = User.objects.filter(is_active = True)
            tos = map(lambda x: x.email, users)
            send_mail(subject = subject, message = body, from_email = from_email, recipient_list = tos)
            return HttpResponse('Eklendi')
    return r('user/create_match.html', {'form' : form}, request)

def leave_info(request):
    return HttpResponse("<h1>akin.kok@akinon.com adresine eposta yolu ile bildiriniz!</h1>")

def leave_match(request, match_id):
    match = get_object_or_404(Match, id = match_id)
    now = datetime.datetime.now()

    if now + settings.MIN_TIME_TO_CANCELATION > match.occured_at:
        raise Http404

    att = Attendance.objects.get(attendee = request.user, match = match)
    att.is_cancelled = True
    att.save()
    return HttpResponseRedirect(reverse('active-match-list'))
    
