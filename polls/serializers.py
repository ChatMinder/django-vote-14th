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
#     #user_login_id = serializers.SerializerMethodField()
#
#     def create(self, validated_data):
#         candidate = Candidate.objects
#         vote = Vote()
#         vote.candidate = candidate
#         try:
#             vote.save(self)
#         except IntegrityError:
#             return vote
#         return vote
#
    class Meta:
        model = Vote
        fields = ('candidates_name',)
#
    def get_candidates_name(self, obj):
        return obj.candidate.name

#     # def get_user_login_id(self, obj):
#     #     return obj.user.login_id
