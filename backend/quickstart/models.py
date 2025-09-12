from django.db import models

# Create your models here.

class Problem(models.Model):
    year = models.IntegerField()
    question_number = models.CharField(max_length = 100)
    domain = models.CharField(max_length = 100)
    statement = models.TextField()

    def __str__(self):
        return f"{self.year} Problem {self.question_number}"

class Solution(models.Model):
    problem = models.ForeignKey(Problem, related_name = 'solutions', on_delete = models.CASCADE)
    hint_level = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Solution for {self.problem} (Level {self.hint_level}"

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
