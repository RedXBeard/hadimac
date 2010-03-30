from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root),
    url(r'^$', 'hadimac.user.views.hadimac_login', name = 'hadimac-login'),
    url(r"^main/$", "django.views.generic.simple.direct_to_template", {"template": "user/main.html"}, name = 'main'),
    url(r'^logout/$', 'hadimac.user.views.hadimac_logout', name = 'hadimac-logout'),
    url(r'^active_matches/$', 'hadimac.mac.views.active_matches', name = 'active-match-list'),
    url(r'^create_match/$', 'hadimac.mac.views.create_match', name = 'create-match'),
    url(r'^enter_match_score/(?P<match_id>\d+)/$', 'hadimac.mac.views.enter_match_score', name = 'enter-match-score'),
    url(r'^attend/(?P<match_id>\d+)/$', 'hadimac.mac.views.attend', name = 'attend'),
    url(r'^how_to_leave/$', 'hadimac.mac.views.leave_info', name = 'leave-info'),
    url(r'^register/$', 'hadimac.user.views.register_step1', name = 'registration'),
    url(r'^register/do/(?P<key>\w+)/$', 'hadimac.user.views.register_step2', name = 'registration-done'),
    url(r'^attendees/(?P<match_id>\d+)/$', 'hadimac.mac.views.attendees', name = 'attendees'),
    url(r'^add/comment/(?P<match_id>\d+)/$', 'hadimac.comment.views.add_comment', name = 'add-comment'),
    url(r'^leave/match/(?P<match_id>\d+)/$', 'hadimac.mac.views.leave_match', name = 'leave-match'),
    url(r'^create/default/user/profiles/$', 'hadimac.user.views.create_default_user_profile',
        name = 'create-default-user-profile'),
    url(r'^email/options/$', 'hadimac.user.views.email_options', name = 'email-options'),
    url(r'^new/match/request/$', 'hadimac.mac.views.new_match_request', name = 'new-match-request'),
    url(r'^requested/match/list/$', 'hadimac.mac.views.requested_match_list', name = 'requested-match-list'),
    url(r'^request/match/(?P<matchrequest_id>\d+)/$', 'hadimac.mac.views.request_match', name = 'request-match'),
    url(r'^requesters/(?P<matchrequest_id>\d+)/$', 'hadimac.mac.views.requesters', name = 'requesters'),
    url(r'^unrequest/(?P<matchrequest_id>\d+)/$', 'hadimac.mac.views.unrequest', name = 'unrequest'),
)
