from django.contrib.auth.models import Group, User
from backend.quickstart.models import Problem, Solution
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
