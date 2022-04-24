from rest_framework import serializers

from problems.models import Problem, Tag, Company, Status
from users.models import User


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

    def __init__(self, *args, **kwargs):
        super(StatusSerializer, self).__init__(*args, **kwargs)
        self.fields['user'] = serializers.HiddenField(default=serializers.CurrentUserDefault())


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'last_login',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
