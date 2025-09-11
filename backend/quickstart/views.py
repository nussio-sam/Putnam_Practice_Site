from django.contrib.auth.models import Group, User
from .models import Problem, Solution
from rest_framework import permissions, viewsets

from backend.quickstart.serializers import GroupSerializer, ProblemSerializer, SolutionSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """API endpoint that allows groups to be viewed or edited"""
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer




