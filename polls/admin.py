from django.contrib import admin

from polls.models import Candidate, Question

admin.site.register(Question)
admin.site.register(Candidate)
#admin.site.register(Vote)
