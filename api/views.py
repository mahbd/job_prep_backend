from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter

from problems.models import Problem
from users.models import User
from .serializers import ProblemSerializer, UserSerializer


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class UserTablePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and (request.user == obj or request.user.is_staff)


# noinspection DuplicatedCode
class ProblemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows problems to be viewed or edited.
    """

    def get_queryset(self):
        problems = Problem.objects.all()
        company = self.request.query_params.get('company')
        tags = self.request.query_params.get('tags')
        if company:
            company = company.split(',')
            problems = problems.filter(companies__overlap=company)
        if tags:
            tags = tags.split(',')
            problems = problems.filter(tags__overlap=tags)
        return problems

    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminUserOrReadOnly]
    filterset_fields = ('difficulty',)
    search_fields = ('name', 'question_html')
    filter_backends = (DjangoFilterBackend, SearchFilter,)

    @action(detail=True, methods=['get'])
    def mark_confident(self, request, pk):
        pk = int(pk)
        user = request.user
        if pk not in user.confident_problems:
            user.confident_problems.append(pk)
        if pk in user.solved_problems:
            user.solved_problems.remove(pk)
        if pk in user.tried_problems:
            user.solved_problems.remove(pk)
        user.save()
        return self.retrieve(request, pk)

    @action(detail=True, methods=['get'])
    def mark_solved(self, request, pk):
        pk = int(pk)
        user = request.user
        if pk not in user.solved_problems:
            user.solved_problems.append(pk)
        if pk in user.confident_problems:
            user.confident_problems.remove(pk)
        if pk in user.tried_problems:
            user.tried_problems.remove(pk)
        user.save()
        return self.retrieve(request, pk)

    @action(detail=True, methods=['get'])
    def mark_tried(self, request, pk):
        pk = int(pk)
        user = request.user
        if pk not in list(user.tried_problems):
            user.tried_problems.append(pk)
        if pk in user.confident_problems:
            user.confident_problems.remove(pk)
        if pk in user.solved_problems:
            user.solved_problems.remove(pk)
        user.save()
        return self.retrieve(request, pk)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [UserTablePermission]
    search_fields = ('username', 'email')
    filterset_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    filter_backends = (SearchFilter, DjangoFilterBackend)
