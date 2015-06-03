from rest_framework import serializers
from policies import models

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Policy
        fields = ('id', 'description')

class And_ruleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.And_rule
        fields = ('id', 'policy', 'description', 'enabled', 'conditions')

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = ('id', 'attribute', 'operator', 'value', 'type', 'description')
