from django.contrib import admin

from hadimac.mac.models import *

admin.site.register(Match)
admin.site.register(Team)
admin.site.register(Score)
admin.site.register(MatchRequest)
admin.site.register(MatchSubstitutes)
