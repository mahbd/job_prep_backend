from rest_framework import serializers

from problems.models import Problem
from users.models import User


class ProblemSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        user = self.context['request'].user
        if obj.id in user.confident_problems:
            return 'Confident'
        elif obj.id in user.solved_problems:
            return 'Solved'
        elif obj.id in user.tried_problems:
            return 'Tried'
        else:
            return 'Untried'

    class Meta:
        model = Problem
        fields = (
            'id', 'name', 'status', 'acceptance', 'difficulty', 'question_html', 'solution_html', 'tags', 'companies')


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
