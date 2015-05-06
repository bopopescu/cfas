from django.db import models

class Attribute_category(models.Model):
    description = models.CharField(max_length=255)

class Operator(models.Model):
    description = models.CharField(max_length=255)

class Cloud_platform(models.Model):
    description = models.CharField(max_length=255)
    accept_negated_conditions = models.BooleanField(default=False)
    operators = models.ManyToManyField(Operator)
    attribute_categories = models.ManyToManyField(Attribute_category)

class Cloud_provider(models.Model):
    description = models.CharField(max_length=255)
    cloud_platform = models.ForeignKey(Cloud_platform)

class Policy(models.Model):
    description = models.CharField(max_length=255)
    cloud_provider = models.ForeignKey(Cloud_provider)

class Condition(models.Model):
    attribute_category = models.ForeignKey(Attribute_category)
    attribute = models.CharField(max_length=255)
    operator = models.ForeignKey(Operator)
    value = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class And_rule(models.Model):
    policy = models.ForeignKey(Policy)
    description = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    conditions = models.ManyToManyField(Condition)
