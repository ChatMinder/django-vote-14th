from django.db import IntegrityError
from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    question_candidate = CandidateSerializer(many=True, read_only=True, source="candidate_set")

    class Meta:
        model = Question
        fields = ['id', 'created_at', 'updated_at', 'question_text', 'question_candidate']


class VoteSerializer(serializers.ModelSerializer):
    candidates_name = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = ('candidates_name',)

    def get_candidates_name(self, obj):
        return obj.candidate.name

