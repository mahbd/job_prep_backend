from rest_framework import serializers

from problems.models import Problem


# class Problem(models.Model):
#     name = models.CharField(max_length=1023)
#     acceptance = models.DecimalField(max_digits=3, decimal_places=2)
#     difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=10)
#     question_html = models.TextField()
#     solution_html = models.TextField()
#     tags = models.ManyToManyField('Tag')
#     companies = models.ManyToManyField('Company')
class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'name', 'acceptance', 'difficulty', 'question_html', 'solution_html', 'tags', 'companies')
