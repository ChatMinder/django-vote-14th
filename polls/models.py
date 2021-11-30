from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Candidate(BaseModel):
    name = models.CharField(max_length=250)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Vote(BaseModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate')

    def save(self, *args, **kwargs):
        self.candidate.votes += 1
        self.candidate.save()
        print(self.candidate.votes)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} voted'.format(self.candidate.name)
