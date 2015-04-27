from django.db import models

class Attribute_categories(models.Model):
    description = models.CharField(max_length=255)

class Operators(models.Model):
    description = models.CharField(max_length=255)

class Cloud_platforms(models.Model):
    description = models.CharField(max_length=255)
    accept_negated_conditions = models.BooleanField(default=False)
    operators = models.ManyToManyField(Operators)
    attribute_categories = models.ManyToManyField(Attribute_categories)

class Cloud_providers(models.Model):
    description = models.CharField(max_length=255)
    cloud_platform = models.ForeignKey(Cloud_platforms)

class Policies(models.Model):
    description = models.CharField(max_length=255)
    cloud_provider = models.ForeignKey(Cloud_providers)
    external_policy = models.TextField()

class Conditions(models.Model):
    attribute_category = models.ForeignKey(Attribute_categories)
    attribute = models.CharField(max_length=255)
    operator = models.ForeignKey(Operators)
    value = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class And_rules(models.Model):
    policy = models.ForeignKey(Policies)
    description = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    conditions = models.ManyToManyField(Conditions)

class Attribute_hierarchy(models.Model):
    superior = models.CharField(max_length=255)
    subordinate = models.CharField(max_length=255)
