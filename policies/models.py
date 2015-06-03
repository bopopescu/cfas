from django.db import models

class Policy(models.Model):
    description = models.CharField(max_length=255)

class Condition(models.Model):
    attribute = models.CharField(max_length=255)
    operator = models.CharField(max_length=1)
    value = models.CharField(max_length=255)
    type = models.CharField(max_length=1)
    description = models.CharField(max_length=255)

class And_rule(models.Model):
    policy = models.ForeignKey(Policy)
    description = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    conditions = models.ManyToManyField(Condition)
