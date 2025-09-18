from django.db import models


class Problem(models.Model):
    year = models.IntegerField()
    question_number = models.CharField(max_length = 100)
    domain = models.CharField(max_length = 100)
    statement = models.TextField()

    def __str__(self):
        return f"{self.year} Problem {self.question_number}"

class Solution(models.Model):
    problem = models.ForeignKey(Problem, related_name = 'solutions', on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Solution for {self.problem}"

# 
class QASession(models.Model):
    question = models.TextField()
    question_context = models.TextField()
    answer = models.TextField()
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Q: {self.question} \n A: {self.answer}"

class StdQuestion(models.Model):
    question_text = models.TextField()
    order = models.IntegerField()
    description = models.TextField(help_text = "What this question gives hints for")
    
    def __str__(self):
        return(f"Q:{self.order}: {self.question_text}")

class ProblemQAResult(models.Model):
    problem = models.ForeignKey(Problem, related_name = 'qa_results' ,on_delete=models.CASCADE)
    solution_level = models.ForeignKey(Solution, related_name = 'qa_results' ,on_delete = models.CASCADE)
    std_question = models.ForeignKey(StdQuestion, on_delete = models.CASCADE)
    gen_answer = models.TextField()
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('problem', 'solution_level', 'std_question')
        ordering = ['problem', 'solution_level__hint_level', 'std_question__order']

    def __str__(self):
        return(f"{self.problem} - Level {self.solution_level.hint_level} - Q {self.std_question.order}") # type: ignore
