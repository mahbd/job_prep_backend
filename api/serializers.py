from rest_framework import serializers

from problems.models import Problem, Tag, Company, Status


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'name', 'acceptance', 'difficulty', 'question_html', 'solution_html', 'tags', 'companies')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'problem', 'user', 'status', 'created_at', 'updated_at')
        read_only_fields = ('user',)

    # add current user to the serializer
    def __init__(self, *args, **kwargs):
        super(StatusSerializer, self).__init__(*args, **kwargs)
        self.fields['user'] = serializers.HiddenField(default=serializers.CurrentUserDefault())
