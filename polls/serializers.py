from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True, source="candidates_set")

    class Meta:
        model = Question
        fields = ['id', 'created_at', 'updated_at', 'question_text', 'candidates']


class VoteSerializer(serializers.ModelSerializer):
    candidates_name = serializers.SerializerMethodField
    user_login_id = serializers.SerializerMethodField

    def create(self, validated_data):
        candidate = get_object_or_404(Candidate, name=validated_data['candidates_name'])
        vote = Vote
        vote.candidate = candidate
        vote.save()

    class Meta:
        model = Vote
        exclude = ['candidate']

    def get_candidates_name(self, obj):
        return obj.candidate.name

    def get_user_id(self, obj):
        return obj.user.login_id
