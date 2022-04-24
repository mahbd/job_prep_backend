from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):
    confident_problems = ArrayField(models.IntegerField(), default=list)
    solved_problems = ArrayField(models.IntegerField(), default=list)
    tried_problems = ArrayField(models.IntegerField(), default=list)
