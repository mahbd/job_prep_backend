from django.db import models

from constants import DIFFICULTY_CHOICES, STATUS_CHOICES
from users.models import User


class Problem(models.Model):
    name = models.CharField(max_length=1023)
    acceptance = models.DecimalField(max_digits=5, decimal_places=2)
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=10)
    question_html = models.TextField()
    solution_html = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    companies = models.ManyToManyField('Company', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-acceptance', 'name']
        verbose_name_plural = 'Problems'
        verbose_name = 'Problem'


class Tag(models.Model):
    name = models.CharField(max_length=1023)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Tags'
        verbose_name = 'Tag'


class Company(models.Model):
    name = models.CharField(max_length=1023)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'
        verbose_name = 'Company'


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default=STATUS_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.problem.name} - {self.status}'

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Statuses'
        verbose_name = 'Status'
