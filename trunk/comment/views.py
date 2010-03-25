from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from hadimac.shortcuts import r
from hadimac.mac.models import Match
from hadimac.comment.models import Comment

import datetime

@login_required
def add_comment(request, match_id):
    if request.POST:
        match = get_object_or_404(Match, pk = match_id)
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        comment = Comment.objects.create(match = match, user = request.user, title = title, content = content)
        return HttpResponseRedirect(reverse('attendees', args=[match_id]))
    else:
        raise Http404
