from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter

from problems.models import Problem, Tag, Company, Status
from .serializers import ProblemSerializer, TagSerializer, CompanySerializer, StatusSerializer


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


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
    filter_backends = (DjangoFilterBackend, SearchFilter)


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminUserOrReadOnly]
    search_fields = ('name',)
    filter_backends = (SearchFilter,)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminUserOrReadOnly]
    search_fields = ('name',)
    filter_backends = (SearchFilter,)


class StatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows statuses to be viewed or edited.
    """

    def get_queryset(self):
        if self.request.user.is_staff:
            return Status.objects.all()
        return Status.objects.filter(user=self.request.user)

    serializer_class = StatusSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    search_fields = ('name',)
    filter_backends = (SearchFilter,)
