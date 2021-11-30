from django.contrib import admin

from polls.models import Candidate, Vote

admin.site.register(Candidate)
admin.site.register(Vote)
