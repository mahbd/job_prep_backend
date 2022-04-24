from django.contrib.postgres.fields import ArrayField
from django.db import models

from constants import DIFFICULTY_CHOICES
from users.models import User


class Problem(models.Model):
    name = models.CharField(max_length=1023)
    acceptance = models.DecimalField(max_digits=5, decimal_places=2)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=10)
    question_html = models.TextField()
    solution_html = models.TextField()
    tags = ArrayField(models.CharField(max_length=1023), default=list)
    companies = ArrayField(models.CharField(max_length=1023), default=list)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-acceptance', 'name']
        verbose_name_plural = 'Problems'
        verbose_name = 'Problem'
