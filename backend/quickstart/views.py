from django.contrib.auth.models import Group, User

from backend.quickstart.serializers import QAReqSerializer, QAResSerializer, QASessionSerializer, SolutionSerializer
from .models import Problem, Solution, QASession


from rest_framework import permissions, viewsets
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

#If someone can find a way to make my pyright not tweak out, please email me
from typing import Dict, Any, cast

from backend.quickstart.ml_service import qa_service


from backend.quickstart.serializers import *

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

#I know this whole project has type: ignores everywhere
#But I promise if you guys dealed with pyright bullshit, you would too
class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all() # type: ignore
    serializer_class = ProblemSerializer

class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all() # type: ignore
    serializer_class = SolutionSerializer

#HuggingFace Views
class QAView(APIView):
    """API Endpoint for QA using roberta"""

    @extend_schema(
        request = QAReqSerializer,
        responses = {200: QAResSerializer}
    )

    def post(self, req):
        if qa_service is None or not qa_service.pipeline_is_ready():
            return Response(
                {'error': f"QA Service is unavailable, check logs"},
                status = status.HTTP_503_SERVICE_UNAVAILABLE
            )

        serializer = QAReqSerializer(data = req.data)

        if serializer.is_valid():
            validated_data = cast(Dict[str, Any], serializer.validated_data)

            question = validated_data['question']
            context = validated_data['context']

            try:
                result = qa_service.answer_question(question, context)

                response_data = {
                        'answer': result['answer'],
                        'confidence': result['confidence'],
                        'start': result['start'],
                        'end': result['end'],
                        'question': question,
                        'context': context
                    }

                return Response(
                        QAResSerializer(response_data).data,
                        status = status.HTTP_200_OK
                    )
            except Exception as exc:
                return Response(
                    {'error': f"Model Inference failure: {str(exc)}"},
                    status = status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(
            serializers.errors, #type: ignore
            status = status.HTTP_400_BAD_REQUEST
        )

class QAHistoryView(generics.ListAPIView):
    """API Endpoint to get qa history"""

    queryset = QASession.objects.all() # type: ignore
    serializer_class = QASessionSerializer

@api_view(['GET'])
def health_check(request):
    """ Health check endpoint for HuggingFace"""

    try:

        test_result = qa_service.answer_question(
        "What is this question?",
        "This is a health check question"
        )
        return Response({
            'status': 'healthy',
            'model': qa_service.model_name,
            'test_confidence': test_result['confidence']
        }, status = status.HTTP_200_OK)
    except Exception as exc:
        return Response({
            'status': 'unhealthy',
            'error': str(exc)
        }, status = status.HTTP_503_SERVICE_UNAVAILABLE )





