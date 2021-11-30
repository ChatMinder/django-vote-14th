
from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(write_only=True)

    def create(self, validated_data):
        candidate = get_object_or_404(Candidate, name=validated_data["candidate_name"])
        vote = Vote()
        vote.candidate = candidate
        vote.save()
        return vote

    class Meta:
        model = Vote
        fields = ('candidate_name',)



