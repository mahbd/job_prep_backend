import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, Case, When
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from constants import COMPANIES
from users.models import User
from .models import Problem


class ProblemListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        problems = Problem.objects.all()
        if self.request.GET.get('company'):
            companies = self.request.GET.getlist('company')
            problems = problems.filter(companies__contains=companies)
        if self.request.GET.get('difficulty'):
            problems = problems.filter(difficulty=self.request.GET.get('difficulty'))
        return problems.annotate(
            status=Case(When(id__in=self.request.user.tried_problems, then=Value('Tried')),
                        When(id__in=self.request.user.solved_problems, then=Value('Solved')),
                        When(id__in=self.request.user.confident_problems, then=Value('Confident')), ))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = COMPANIES
        context['company'] = self.request.GET.get('company')
        return context

    paginate_by = os.getenv('PROBLEMS_PER_PAGE', 10)


class ProblemDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Problem.objects.all().annotate(
            status=Case(When(id__in=self.request.user.tried_problems, then=Value('Tried')),
                        When(id__in=self.request.user.solved_problems, then=Value('Solved')),
                        When(id__in=self.request.user.confident_problems, then=Value('Confident')), ))


def mark_problem(request, pk, mark):
    user: User = request.user
    if pk in user.confident_problems:
        user.confident_problems.remove(pk)
    if pk in user.solved_problems:
        user.solved_problems.remove(pk)
    if pk in user.tried_problems:
        user.tried_problems.remove(pk)
    if mark == 'confident':
        user.confident_problems.append(pk)
    elif mark == 'solved':
        user.solved_problems.append(pk)
    elif mark == 'tried':
        user.tried_problems.append(pk)
    user.save()
    return redirect('problems:problem_detail', pk=pk)
