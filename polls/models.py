from django.db import models
from api.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Question(BaseModel):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Candidate(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# class Vote(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
#     candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate')
#
#     def save(self, *args, **kwargs):
#         self.candidate.votes += 1
#         self.candidate.save()
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return '{} -> {}'.format(self.user.login_id, self.candidate.name)

