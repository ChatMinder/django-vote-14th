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
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    name = models.CharField(max_length=250)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Vote(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vote')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate')

    def __str__(self):
        return self.user.login_id

