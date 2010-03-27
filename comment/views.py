from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db import transaction

from hadimac.shortcuts import r
from hadimac.mac.models import Match
from hadimac.comment.models import Comment

import datetime

@login_required
@transaction.commit_on_success
def add_comment(request, match_id):
    if request.POST:
        if Comment.objects.filter(user = request.user,
                                  created_at__gte = datetime.datetime.now() -\
                                      datetime.timedelta(minutes = 0)):
            return HttpResponse(u"Bir on dakika mola verirsen pek cool olur.")
        match = get_object_or_404(Match, pk = match_id)
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        comment = Comment.objects.create(match = match, user = request.user, title = title, content = content)

        subject = u"%s, %s tarihli maca yorum yazdi." % (request.user.get_full_name(), match.occured_at.date().__str__())
        body = "%s\n\n%s\n\nhttp://hadimac.test.akinon.com%s adresinde yorumun icerigini bulabilirsiniz."%(title,
                                                                                      content,
                                                                                      reverse('attendees', args=[match_id]))
        from_email = "hadimac@akinon.com"
        users = auth.models.User.objects.filter(is_active = True, userprofile__get_forum_activity_as_email = True)
        print users
        tos = map(lambda x: x.email, users)
        send_mail(subject = subject, message = body, from_email = from_email, recipient_list = tos)
        return HttpResponseRedirect(reverse('attendees', args=[match_id]))
    else:
        raise Http404
