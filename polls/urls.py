from django.urls import path
from rest_framework import routers

from polls import views

urlpatterns = [
    path('votes', views.CastVote.as_view()),
    path('candidates', views.CandidateList.as_view()),
    path('candidates/<int:pk>', views.CandidateDetail.as_view())
]
