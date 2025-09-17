from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from backend.quickstart.models import Problem, Solution, QASession, ProblemQAResult, StdQuestion
from backend.quickstart.serializers import ProblemSerializer, SolutionSerializer, QAReqSerializer, QAResSerializer, ProblemQAResultSerializer, StdQuestionSerializer

#Test suite for integration of problem model data
#----------------------------------------------------------------------------------------------------------------------
class ProblemModelTest(TestCase):
    def setUp(self):
        self.problem = Problem.objects.create(
            year = 1970,
            question_number = 'A2',
            domain = 'math',
            statement = 'hello!'
        )
        self.problem.save()
    
    def test_problem_creation(self):
        """Test self.problem exists and there is only one"""
        self.assertEqual(Problem.objects.count(), 1)

    def test_problem_fields(self):
        """Test all fields of self.problem exist and match the creation"""
        self.assertEqual(self.problem.year, 1970)
        self.assertEqual(self.problem.question_number, 'A2')
        self.assertEqual(self.problem.domain, 'math')
        self.assertEqual(self.problem.statement, 'hello!')
    
class ProblemAPITest(APITestCase):
    def setUp(self):
        self.problem = Problem.objects.create(   
            year = 1970,
            question_number = 'A2',
            domain = 'math',
            statement = 'hello!'
        )

        self.list_url = reverse('problem-list')
        self.detail_url = reverse('problem-detail', args=[self.problem.id])

    def test_list_problems(self):
        """Ensure GET without ID returns the correct list"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Just makin sure there's only one returned item
        self.assertEqual(len(response.json()), 1)

    def test_create_problem(self):
        """Ensure POST creates a new problem correctly and updates DB"""
        data = {
            'year': 2025,
            'question_number': 'B2',
            'domain': 'combinatorics',
            'statement': '3 factorial'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Problem.objects.count(), 2)

    def test_retrieve_problem(self):
        """Ensure GET with id returns a single problem (and serializer works correctly)"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()['question_number'], 'A2')


#Test suite for integration of solution model data
#----------------------------------------------------------------------------------------------------------------------



