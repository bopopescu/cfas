from django.db import models

class Policy(models.Model):
    description = models.CharField(max_length=255)

class Condition(models.Model):
    attribute = models.CharField(max_length=255)
    operator = models.CharField(max_length=50)
    value = models.CharField(max_length=255)
    type = models.CharField(max_length=1)
    description = models.CharField(max_length=255)

class And_rule(models.Model):
    policy = models.ForeignKey(Policy)
    description = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    conditions = models.ManyToManyField(Condition)

class Attribute(models.Model):
    policy = models.ForeignKey(Policy)
    attribute = models.CharField(max_length=255)

class Value(models.Model):
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(max_length=255)

class Hierarchy(models.Model):
    parent = models.ForeignKey(Value, related_name='parent')
    child = models.ForeignKey(Value, related_name='child')
