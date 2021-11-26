from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField
    user_login_id = serializers.SerializerMethodField

    def create(self, validated_data):
        candidate = get_object_or_404(Candidate, name=validated_data['candidate_name'])
        vote = Vote
        vote.candidate = candidate
        vote.save()

    class Meta:
        model = Vote
        fields =['candidate_name', 'user_login_id']

    def get_candidate_name(self, obj):
        return obj.candidate.name

    def get_user_login_id(self, obj):
        return obj.user.login_id
