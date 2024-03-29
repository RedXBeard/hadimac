# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings

from hadimac.mac.models import Match, MatchRequest, Score ,MatchSubstitutes
from hadimac.comment.models import Comment
from hadimac.shortcuts import r
from hadimac.mac.forms import MatchForm, MatchTeamForm, Team, MatchRequestForm, MatchScoreForm ,MatchSubstitute
from hadimac.user.models import Attendance, UserFault, UserProfile, MatchRequestAttendance

import datetime , random ,sha

@login_required
def active_matches(request):
    now = datetime.datetime.now()

    active_matches = list(Match.objects.filter(is_active = True).order_by('-occured_at'))
    for match in active_matches:
        match.is_attended = Attendance.is_user_attended(request.user, match)
        match.number_of_att = match.attendance_set.filter(is_cancelled = False).count()
        match.is_old = match.occured_at < now

    passive_matches = list(Match.objects.filter(is_active = False).order_by('-occured_at'))
    for match in passive_matches:
        match.is_attended = Attendance.is_user_attended(request.user, match)
        match.number_of_att = match.attendance_set.filter(is_cancelled = False).count()
        match.is_old = match.occured_at < now
    teamform = MatchTeamForm()
    scoreform = MatchScoreForm()
    form = MatchSubstitute()
    return r('user/match_list.html', {'active_matches' : active_matches, 
                                      'passive_matches' : passive_matches, 
                                      'teamform' : teamform,
                                      'scoreform' : scoreform,
                                      'form':form }, request)

@login_required
def attendees(request, match_id):
    match = get_object_or_404(Match, id = match_id)
    comments = Comment.objects.filter(match = match, is_visible = True).order_by('created_at')
    home_players = match.home_team.attendance_set.filter(is_cancelled = False, match = match)
    away_players = match.away_team.attendance_set.filter(is_cancelled = False, match = match)

    if match.home_team.attendance_set.filter(is_cancelled = False, match = match, attendee=request.user):
        users_team = "home"
    elif match.away_team.attendance_set.filter(is_cancelled = False, match = match, attendee=request.user):
        users_team = "away"
    else:
        users_team = "none"
    if request.POST.get('formation'):
      match.formation = request.POST.get('formation')
      match.save()
      return HttpResponse(u'Kaydedildi')
    return r('user/attendees.html', {'match' : match,
                                      'users_team' : users_team,
                                      'home_players' : home_players,
                                      'away_players' : away_players,
                                      'comments' : comments,
                                      'score' : match.score_set.all()}, request)

@login_required
def attend(request, match_id):
    if request.POST:
        match = get_object_or_404(Match, id = match_id)

        try   : team = get_object_or_404(Team, id = request.POST.get('team', 0))
        except: return HttpResponse("Takim seciniz...")

        now = datetime.datetime.now()
        if match.occured_at < now -  settings.MIN_TIME_TO_CANCELATION or\
                UserFault.objects.filter(owner = request.user, match__occured_at__gte = now - settings.LENGTH_OF_FAULT):
            return HttpResponse("Cezaniz var.")

        if match.attendance_set.filter(is_cancelled = False).count() >= match.stack:
            return HttpResponse(u'Aktivite Dolu!')

        if team.attendance_set.filter(match = match, is_cancelled = False).count() >= (match.stack / 2):
            return HttpResponse(u'Takım Dolu!')

        if not Attendance.is_user_attended(request.user, match):
            obj, is_created = Attendance.objects.get_or_create(attendee = request.user, match = match)
            obj.is_cancelled = False
            obj.team = team
            obj.save()
        return HttpResponseRedirect(reverse('active-match-list'))

    else:
        return HttpResponse(u'Takım Seçin!')

def create_match_cronic(request):
    u = User.objects.get(email='serdar@yuix.org')
    import time
    delta_days_to_wed = (2 - datetime.datetime.now().weekday() + 7) % 7
    occuredat = datetime.datetime.fromtimestamp(time.time()+delta_days_to_wed * 24 * 60 * 60)
    occuredat = occuredat.replace(hour=20,minute=0,second=0)
    from hadimac.mac.models import Team as Teams
    teams = Teams.objects.all()
    match = Match.objects.create(occured_at = occuredat,
                                    place = u"Feriköy Halısaha",
                                    creater = u,
                                    stack = 14,
                                    home_team = teams[0],
                                    away_team = teams[1])
    if UserProfile.objects.get(user = u).get_match_activity_as_email:
        subject = u"%s tarihinde oynanacak maç sistemde açıldı." % match.occured_at.date().__str__()
        body = u"Oynamak isteyenler lütfen sistemden kayıt olunuz. \n\n http://hadimac.test.akinon.com" 
        from_email = "hadimac@akinon.com"
        users = User.objects.filter(is_active = True)
        tos = map(lambda x: x.email, users)
        send_mail(subject = subject, message = body, from_email = from_email, recipient_list = tos)
    
    return HttpResponse('Eklendi')


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
            if UserProfile.objects.get(user = request.user).get_match_activity_as_email:
                subject = u"%s tarihinde oynanacak maç sistemde açıldı." % match.occured_at.date().__str__()
                body = u"Oynamak isteyenler lütfen sistemden kayıt olunuz. \n\n http://hadimac.test.akinon.com" 
                from_email = "hadimac@akinon.com"
                users = User.objects.filter(is_active = True)
                tos = map(lambda x: x.email, users)
                send_mail(subject = subject, message = body, from_email = from_email, recipient_list = tos)
            return HttpResponse('Eklendi')
    return r('user/create_match.html', {'form' : form}, request)

@login_required
def leave_info(request):
    return HttpResponse("<h1>akin.kok@akinon.com adresine eposta yolu ile bildiriniz!</h1>")

@login_required
def leave_match(request, match_id):
    # raise Http404() # this was just a joke
    match = get_object_or_404(Match, id = match_id)
    now = datetime.datetime.now()

    if now + settings.MIN_TIME_TO_CANCELATION > match.occured_at:
        raise Http404

    att = Attendance.objects.get(attendee = request.user, match = match)
    att.is_cancelled = True
    att.save()
    return HttpResponseRedirect(reverse('active-match-list'))
    
@login_required
def new_match_request(request):
    form = MatchRequestForm()
    if request.POST:
        form = MatchRequestForm(request.POST)
        if form.is_valid() and form.validate():
            data = form.cleaned_data
            mr = MatchRequest(
                home_team = data['home_team'],
                away_team = data['away_team'],
                occured_at = data['occured_at'],
                place = data['place'],
                creater = request.user,
                stack = data['stack'],
                explanation = data['explanation'])
            mr.save()
            return HttpResponse('Maç Önerildi')
    return r("user/match_request.html", {"form" : form}, request)

@login_required
def requested_match_list(request):
    match_list = MatchRequest.objects.filter(occured_at__gte = datetime.datetime.now())
    for mq in match_list:
        mq.number_of_att = mq.matchrequestattendance_set.filter(is_cancelled = False).count()
        mq.is_attended = MatchRequestAttendance.objects.filter(attendee = request.user, is_cancelled = False)
    return r("user/requested_match_list.html", {"list" : match_list, "form" : MatchTeamForm()}, request)

@login_required
def request_match(request, matchrequest_id):
    mq = get_object_or_404(MatchRequest, pk = matchrequest_id)

    team = get_object_or_404(Team, id = request.POST.get('team', None))

    if not team: 
        raise Http404

    now = datetime.datetime.now()
    if mq.occured_at < now -  settings.MIN_TIME_TO_CANCELATION or\
            UserFault.objects.filter(owner = request.user, match__occured_at__gte = now - datetime.timedelta(days = 7)):
        raise Http404

    if mq.matchrequestattendance_set.filter(is_cancelled = False).count() >= mq.stack:
        return HttpResponse(u'Aktivite Dolu!')

    if team.matchrequestattendance_set.filter(match_request = mq, is_cancelled = False).count() >= (mq.stack / 2):
        return HttpResponse(u'Takım Dolu!')
     
    if not MatchRequestAttendance.is_user_attended(request.user, mq):
        obj, is_created = MatchRequestAttendance.objects.get_or_create(attendee = request.user, match_request = mq)
        obj.is_cancelled = False
        obj.team = team
        obj.save()
    return HttpResponseRedirect(reverse('requested-match-list'))

@login_required
def requesters(request, matchrequest_id):
    return HttpResponse("<br/><br/>".join(map(lambda x: unicode(x), MatchRequestAttendance.objects.filter(match_request__id = matchrequest_id, is_cancelled = False))))

@login_required
def unrequest(request, matchrequest_id):
    mra = get_object_or_404(MatchRequestAttendance, attendee = request.user)
    mra.is_cancelled = True
    mra.save()
    return HttpResponseRedirect(reverse('requested-match-list'))

@login_required
def enter_match_score(request, match_id):
    if request.POST:
        form = MatchScoreForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            match = get_object_or_404(Match, pk = match_id)
            score = Score.objects.create(match = match, home_score = data['home_score'], away_score = data['away_score'])
            match.is_active = False
            match.save()
            return HttpResponse(u'Maç Skoru Girildi.')
        else:
            return HttpResponse(u'Doğru Formatta Skor Giriniz!')
    else:
        return HttpResponse(u'Maç Skoru Giriniz!')
      
@login_required
def substitute(request, match_id):
		if request.POST:
			form = MatchSubstitute(request.POST)
			if form.is_valid():
			    data = form.cleaned_data
			    key = MatchSubstitutes(email = data['email'], inviter = request.user).create_key()
			    current_site = Site.objects.get_current()
			    domain = current_site.domain
			    mail = EmailMultiAlternatives(u"Yerime Oynarmısın?",
			                                  u'%s kendisini en iyi temsil eden kişi olarak seni seçti <br> Eğer Teklifini Kabul Ediyorsan <br> Aşağıdaki linke tıklayın.<br><a href="http://%s%s">Tıklayın!</a>'%(request.user,domain, reverse('substitute1', args = [key])),
			                                  "hadimac@markafoni.com",
			                                  [data['email']])
			    mail.content_subtype = "html"
			    mail.send()
		return HttpResponseRedirect(reverse('main', args=[]))
		
@login_required
def substitute1(request, key):
		proposal = get_object_or_404(MatchSubstitutes,key = key , is_active = True)
		proposal.is_active = False
		proposal.save()

		inv = Attendance.objects.get(attendee = proposal.inviter)
		if not Attendance.is_user_attended(request.user, inv.match):
			subs = Attendance(attendee = request.user, match = inv.match ,team = inv.team, is_cancelled = False)
			subs.save()
			inv.delete()
			
			mail = EmailMultiAlternatives(u"Yerine Adam bulundu",
			                              u'%s teklifini kabul etti<br>'%(request.user),
			                              "hadimac@markafoni.com",
			                              [proposal.email])
			mail.content_subtype = "html"
			mail.send()
			return HttpResponseRedirect("?next=%s"%reverse('substitute1', args = [key]))
