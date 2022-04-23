from django.contrib import admin

from .models import Problem, Tag, Company, Status


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'acceptance', 'difficulty',)
    list_filter = ('tags', 'companies', 'difficulty', 'acceptance',)
    search_fields = ('name', 'question_html',)
    list_per_page = 20


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'status', 'updated_at',)
    list_filter = ('status', 'problem', 'user', 'updated_at',)
    search_fields = ('user__username', 'problem__name',)
