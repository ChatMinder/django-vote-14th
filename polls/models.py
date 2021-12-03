from django.db import models
from api.models import BaseModel


class Candidate(BaseModel):
    name = models.CharField(max_length=250, null=False, blank=False)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Vote(BaseModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate')

    def save(self, *args, **kwargs):
        self.candidate.votes += 1
        self.candidate.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} voted'.format(self.candidate.name)
