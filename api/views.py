from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from problems.models import Problem
from .serializers import ProblemSerializer


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class ProblemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows problems to be viewed or edited.
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminUserOrReadOnly]
    filterset_fields = ('tags', 'difficulty', 'companies')
    search_fields = ('name', 'question_html')
    filter_backends = (DjangoFilterBackend,)
