from django.contrib.auth.models import Group, User
from backend.quickstart.models import Problem, ProblemQAResult, Solution, QASession, StdQuestion
from rest_framework import serializers

# Serializers for external hyperlinked models
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


# Serializers for all models within the .models.py module
class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        id = ['id', 'year', 'question_number', 'domain', 'statement']

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        id = ['id', 'problem', 'hint_level', 'content', 'created_at']

# Serializers for HuggingFace req/res models

class QAReqSerializer(serializers.Serializer):
    question = serializers.CharField(max_length = 500, required = True)
    question_context = serializers.CharField(required = True)


class QAResSerializer(serializers.Serializer):
    answer = serializers.CharField()
    confidence = serializers.FloatField()
    start = serializers.IntegerField(allow_null = True)
    end = serializers.IntegerField(allow_null = True)
    question = serializers.CharField()
    question_context = serializers.CharField()


class QASessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QASession
        fields = ['id', 'question', 'context', 'answer', 'confidence', 'created_at']
        read_only_fields = ['id', 'created_at']

class StdQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StdQuestion
        fields = ['id', 'question_text', 'order', 'description']
        read_only_fields = ['id']

class ProblemQAResultSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer(read_only = True)
    solution_level = SolutionSerializer(read_only = True)
    std_question = StdQuestionSerializer(read_only = True)

    class Meta:
        model = ProblemQAResult
        fields = [
            'id', 'problem', 'solution_level', 'std_question', 'gen_answer', 'confidence', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
