from django.urls import path

from . import views

app_name = 'problems'

urlpatterns = [
    path('', views.ProblemListView.as_view(), name='problem_list'),
    path('<int:pk>/', views.ProblemDetailView.as_view(), name='problem_detail'),
    path('<int:pk>/add-link/', views.add_problem_link, name='add_problem_link'),
    path('<int:pk>/<str:mark>/', views.mark_problem, name='mark_problem'),
]
