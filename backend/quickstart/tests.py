from datetime import datetime
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
        self.detail_url = reverse('problem-detail', args=[self.problem.id]) # type: ignore
        #I ignore that because I don't wanna set up a stub for auto-incrementing IDs at compile time

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

class SolutionModelTest(TestCase):
    def setUp(self):
        self.foreign_problem = Problem.objects.create(
            year = 1970,
            question_number = 'A2',
            domain = 'math',
            statement = 'a^2 + b^2 = c^2'
        )

        # datetime.now() method instantiates at every call
        #So it's easier to consolidate it to one variable that can be recalled
        self.date = datetime.now() 
        self.solution = Solution.objects.create(
            problem = self.foreign_problem,
            content = 'This is the pythagorean theorem',
            created_at = self.date
        )
        

    def test_solution_creation(self):
        """Test self.solution exists and there is only one"""
        self.assertEqual(Solution.objects.count(), 1)

    def test_solution_fields(self):
        """Test all fields of self.solution and foreign key exist and match the creation"""
        self.assertEqual(self.foreign_problem.year, 1970)
        self.assertEqual(self.foreign_problem.question_number, 'A2')
        self.assertEqual(self.foreign_problem.domain, 'math')
        self.assertEqual(self.foreign_problem.statement, 'a^2 + b^2 = c^2')
        
        self.assertEqual(self.solution.problem, self.foreign_problem)
        self.assertEqual(self.solution.content, 'This is the pythagorean theorem')
        self.assertEqual(self.solution.created_at, self.date)

class SolutionAPITest(TestCase):
    def setUp(self):
        
        self.foreign_problem = Problem.objects.create(
            year = 1970,
            question_number = 'A2',
            domain = 'math',
            statement = 'a^2 + b^2 = c^2'
        )

        self.date = datetime.now() 
        self.solution = Solution.objects.create(
            problem = self.foreign_problem,
            content = 'This is the pythagorean theorem',
            created_at = self.date
        )
        
        self.list_url = reverse('solution-list')
        self.detail_url = reverse('solution-detail', args=[self.solution.id] ) # type: ignore
    def test_list_solutions(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_list_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        self.assertEqual(response.json()['problem'], self.foreign_problem )




