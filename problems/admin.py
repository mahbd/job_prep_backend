from django.contrib import admin

from .models import Problem


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'acceptance', 'difficulty',)
    list_filter = ('difficulty',)
    search_fields = ('name', 'question_html',)
    list_per_page = 20
