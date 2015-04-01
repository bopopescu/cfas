from django.db import models

class Attribute_type(models.Model):
    description = models.CharField(max_length=255)

class Operator(models.Model):
    description = models.CharField(max_length=255)

class Cloud_platform(models.Model):
    description = models.CharField(max_length=255)
    accept_negated_conditions = models.BooleanField(default=False)
    operators = models.ManyToManyField(Operator)
    attribute_types = models.ManyToManyField(Attribute_type)

class Cloud_provider(models.Model):
    description = models.CharField(max_length=255)
    cloud_platform_id = models.ForeignKey(Cloud_platform)

class Policy(models.Model):
    description = models.CharField(max_length=255)
    cloud_provider_id = models.ForeignKey(Cloud_provider)
    external_policy_id = models.CharField(max_length=255)

class Condition(models.Model):
    negated = models.BooleanField(default=False)
    attribute_type_id = models.ForeignKey(Attribute_type)
    attribute = models.CharField(max_length=255)
    operator_id = models.ForeignKey(Operator)
    value = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class And_rule(models.Model):
    policy_id = models.ForeignKey(Policy)
    description = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    conditions = models.ManyToManyField(Condition)
